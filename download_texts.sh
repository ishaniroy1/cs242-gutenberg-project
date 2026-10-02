#!/usr/bin/env bash

mkdir -p gutenberg_texts

# Dostoyevsky - Notes from the Underground
curl -fsSL -o gutenberg_texts/underground.txt https://www.gutenberg.org/cache/epub/600/pg600.txt

# Kafka - The Metamorphosis
curl -fsSL -o gutenberg_texts/metamorphosis.txt https://www.gutenberg.org/cache/epub/5200/pg5200.txt

total=$(cat gutenberg_texts/*.txt | wc -c)
echo "Downloaded $((total / 1024)) KB"
