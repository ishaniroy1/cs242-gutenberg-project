from parsing import underground_processed, metamorphosis_processed

import numpy as np
import pandas as pd

def build_counts(books, names):

    labels, token_lists = [], []

    for name, docs in zip(names, books):
        for idx, section in enumerate(docs):
            labels.append(f"{name}_{idx+1}")
            token_lists.append(section)

    vocab = sorted({t for tokens in token_lists for t in tokens})
    term_to_col = {t: i for i, t in enumerate(vocab)}

    matrix = np.zeros((len(token_lists), len(vocab)), dtype=np.int64)
    for row, tokens in enumerate(token_lists):
        terms, freqs = np.unique(tokens, return_counts=True)
        matrix[row, [term_to_col[t] for t in terms]] = freqs

    return pd.DataFrame(matrix, index=labels, columns=vocab)

def calc_tf(counts):
    return counts.div(counts.sum(axis=1), axis=0)

def calc_idf(counts):
    num_docs = len(counts)
    num_t = (counts > 0).sum().to_numpy()
    return pd.Series(np.log(num_docs / (1 + num_t)), index=counts.columns)

def calc_tfidf(counts):
    tf = calc_tf(counts)
    idf = calc_idf(counts)
    return pd.DataFrame(tf.to_numpy() * idf.to_numpy(), index=counts.index, columns=counts.columns)


counts = build_counts(
        [underground_processed, metamorphosis_processed],
        ["underground", "metamorphosis"]
)
tfidf = calc_tfidf(counts)

"""
print(tfidf.head())
print(counts.shape)
print(tfidf.shape)
print(max(tfidf))
"""
