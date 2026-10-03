from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from parsing import underground_processed, metamorphosis_processed
from tf_idf import build_counts, calc_tfidf

OUT = Path("analysis")
OUT.mkdir(exist_ok=True)

BOOKS = {
    "underground": underground_processed,
    "metamorphosis": metamorphosis_processed,
}
# a term that only appears once is uninformative
MIN_TOTAL = 2  

def book_of(index):
    return pd.Series(index.str.rsplit("_", n=1).str[0], index=index)


def tfidf_for(books, n=1):

    def to_ngrams(tokens):
        return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

    ngram_books = [[to_ngrams(section) for section in docs] for docs in books.values()]
    counts = build_counts(ngram_books, list(books))
    return counts, calc_tfidf(counts)


# highest TF-IDF terms
def top_term_per_doc(tfidf, counts):
    keep = counts.sum(axis=0) >= MIN_TOTAL
    ranked = tfidf.loc[:, keep]
    return pd.DataFrame({"term": ranked.idxmax(axis=1), "tfidf": ranked.max(axis=1).round(4)})

def top_terms_per_book(tfidf, counts, n=10):
    keep = counts.sum(axis=0) >= MIN_TOTAL
    books = book_of(tfidf.index)
    return {b: tfidf.loc[books == b, keep].mean().nlargest(n) for b in books.unique()}


def plot_top_term_per_doc(top1, path):
    books = book_of(top1.index)
    colors = dict(zip(books.unique(), plt.cm.tab10.colors))
    fig, ax = plt.subplots(figsize=(8, 0.3 * len(top1) + 1.5))
    ax.barh(range(len(top1)), top1["tfidf"], color=[colors[b] for b in books])
    ax.set_yticks(range(len(top1)))
    ax.set_yticklabels([f"{d}: {t}" for d, t in zip(top1.index, top1["term"])], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("TF-IDF of the document's top term")
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in colors.values()],
              labels=list(colors), loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_top_terms_per_book(book_terms, path):
    fig, axes = plt.subplots(1, len(book_terms), figsize=(5 * len(book_terms), 4))
    for ax, (book, series) in zip(np.atleast_1d(axes), book_terms.items()):
        ax.barh(series.index[::-1], series.to_numpy()[::-1])
        ax.set_title(f"Top terms in {book}")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# similarity between documents
def cosine_similarity(tfidf):
    X = np.clip(tfidf.to_numpy(), 0, None)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X = X / np.where(norms == 0, 1, norms)
    return pd.DataFrame(X @ X.T, index=tfidf.index, columns=tfidf.index)


def book_similarity_table(sim):
    books = book_of(sim.index)
    names = books.unique()
    table = pd.DataFrame(index=names, columns=names, dtype=float)
    S = sim.to_numpy()
    for a in names:
        for b in names:
            block = S[np.ix_((books == a).to_numpy(), (books == b).to_numpy())]
            if a == b:
                n = len(block)
                block = block[~np.eye(n, dtype=bool)] if n > 1 else np.array([np.nan])
            table.loc[a, b] = np.nanmean(block)
    return table


def plot_heatmap(sim, path):
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(sim.to_numpy(), cmap="viridis")
    ax.set_xticks(range(len(sim)))
    ax.set_xticklabels(sim.index, rotation=90, fontsize=6)
    ax.set_yticks(range(len(sim)))
    ax.set_yticklabels(sim.index, fontsize=6)
    fig.colorbar(im, ax=ax, label="cosine similarity (TF-IDF)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# k-means and 2d projection
def kmeans(X, k, n_init=20, n_iter=100, seed=0):
    rng = np.random.default_rng(seed)
    best_labels, best_inertia = None, np.inf
    for _ in range(n_init):
        centers = X[rng.choice(len(X), k, replace=False)]
        for _ in range(n_iter):
            d = (X ** 2).sum(1)[:, None] - 2 * X @ centers.T + (centers ** 2).sum(1)[None, :]
            labels = d.argmin(axis=1)
            new = np.array([X[labels == j].mean(axis=0) if (labels == j).any() else centers[j]
                            for j in range(k)])
            if np.allclose(new, centers):
                break
            centers = new
        inertia = d[np.arange(len(X)), labels].sum()
        if inertia < best_inertia:
            best_labels, best_inertia = labels, inertia
    return best_labels


def cluster_documents(tfidf, k):
    X = np.clip(tfidf.to_numpy(), 0, None)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X = X / np.where(norms == 0, 1, norms)
    labels = kmeans(X, k)
    return pd.Series(labels, index=tfidf.index, name="cluster")

# main
if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 60)

    # tf-idf
    counts, tfidf = tfidf_for(BOOKS, n=1)
    print(f"Corpus: {counts.shape[0]} sections, {counts.shape[1]} unique terms\n")

    top1 = top_term_per_doc(tfidf, counts)
    print("Highest TF-IDF term per document:")
    print(top1.to_string(), "\n")
    plot_top_term_per_doc(top1, OUT / "top_term_per_document.png")

    book_terms = top_terms_per_book(tfidf, counts, n=10)
    print("Top terms per book (mean TF-IDF):")
    for b, s in book_terms.items():
        print(f"  {b}: {', '.join(s.index)}")
    print()
    plot_top_terms_per_book(book_terms, OUT / "top_terms_per_book.png")

    # similarity    
    sim = cosine_similarity(tfidf)
    plot_heatmap(sim, OUT / "similarity_heatmap.png")
    book_sim = book_similarity_table(sim)    
    print("Mean cosine similarity between books (diagonal = within book):")
    print(book_sim.round(4), "\n")

    # clustering    
    clusters = cluster_documents(tfidf, k=len(BOOKS))
    print("k-means clusters vs true book (rows = book, columns = cluster):")
    print(pd.crosstab(book_of(tfidf.index), clusters), "\n")

    # n-grams
    summary, top_by_n = [], {}
    for n in (1, 2):
        c, t = (counts, tfidf) if n == 1 else tfidf_for(BOOKS, n=n)
        s = cosine_similarity(t)
        bs = book_similarity_table(s)
        within = np.nanmean(np.diag(bs.to_numpy()))
        between = np.nanmean(bs.to_numpy()[~np.eye(len(bs), dtype=bool)]) if len(bs) > 1 else np.nan
        summary.append({
            "n": n,
            "vocabulary": c.shape[1],
            "% seen in 1 section only": round(100 * ((c > 0).sum(axis=0) == 1).mean(), 1),
            "mean within-book similarity": round(within, 4),
            "mean between-book similarity": round(between, 4),
        })
        top_by_n[n] = top_terms_per_book(t, c, n=8)

    summary = pd.DataFrame(summary)
    print("unigram vs bigram TF-IDF:")
    print(summary.to_string(index=False), "\n")

    for b in BOOKS:
        table = pd.DataFrame({f"{n}-gram": list(top_by_n[n][b].index) for n in (1, 2)})
        print(f"Top unigram and bigram for {b}:")
        print(table.to_string(index=False), "\n")

    print(f"Tables and figures saved in {OUT}")
