# CS24200: Project 1 - TF-IDF

Parse Project Gutenberg ebooks using regex, calculate TF-IDF from scratch with NumPy and pandas, and analyze documents using TF-IDF.
- *Notes from the Underground* by Fyodor Dostoyevsky
- *The Metamorphosis* by Franz Kafka

Each chapter is counted as one document. There are 21 from *Notes from the Underground* across two parts and 3 from *The Metamorphosis*. I found each document's highest-scoring term (essentially the most distinctive term) and cosine similarity between documents (how similar the vocabulary is between two texts). A cosine score close to 1 can be interpreted as the two documents having highly similar content, while a cosine score close to 0 means that the documents share almost no meaningful words. Finally, I grouped the documents with k-means and compared unigram and bigram TF-IDF.

## Prerequisites
- Python 3.10+
- `bash` and `curl` (on Windows, use Windows Subsystem for Linux)
- Python packages: `numpy`, `pandas`, `nltk`, and `matplotlib`

## Setup Instructions

You can download the required assets automatically using the provided setup script.

```bash
python -m venv venv
source venv/bin/activate
pip install numpy pandas nltk matplotlib
```

## Running the project

Run everything from the project's root folder using the run pipeline.

```bash
python run_pipeline.py
```

## Output

`analysis.py` prints the following information to the terminal:
- The top TF-IDF term for each document
- The top terms for each book
- Mean cosine similarity within and between books (how similar the vocabulary is within/between the texts)
- A table of k-means clusters
- A unigram vs. bigram comparison and the top terms of each one

It saves three figures to `analysis/`:
- `top_term_per_document.png`
- `top_terms_per_book.png`
- `similarity_heatmap.png`

## Project structure

| File | Purpose |
| --- | --- |
| `download_gutenberg.sh` | Downloads the two plain-text books |
| `parsing.py` | Strips any information not part of the book, splits the text into chapters, cleans and tokenizes, removes stopwords, and stems the plain-text files |
| `tf_idf.py` | Builds the term-count matrix and computes TF-IDF |
| `analysis.py` | Finds top terms, similarity, clustering, and compares n-grams with figures |
| `run_pipeline.py` | Can be executed with `python run_pipeline.py` to run the project end-to-end |
| `gutenberg_texts/` | Downloaded books |
| `analysis_output/` | Figures created by `analysis.py` |
