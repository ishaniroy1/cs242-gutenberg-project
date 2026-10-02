from pathlib import Path
from itertools import islice
import pandas as pd
import re

# for stopword removal and stemming
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# path to full text files
u_path = Path("gutenberg_texts") / "underground.txt"
m_path = Path("gutenberg_texts") / "metamorphosis.txt"


# splits at the start and end of the ebook as defined by Project Gutenberg
def clean_ebook_start_end(ebook_path, start, end):

    with open(ebook_path, "r", encoding="utf-8") as file:
        ebook_full = file.read()

    try:
        ebook = ebook_full.split(start)[1].split(end)[0].strip()
    except IndexError:
        print("One or both markers were not found in the file.")
    return ebook


# split chapters/parts (both use roman numerals)
def split_by_roman_numerals(text):

    ROMAN_LINE = re.compile(r"^[ \t]*([IVXLC]+)[ \t]*$", re.MULTILINE)
    PART_LINE = re.compile(r"^[ \t]*PART\b.*$", re.MULTILINE)
    SUBTITLE = re.compile(r"^[ \t]*À Propos of the Wet Snow[ \t]*$", re.MULTILINE)

    matches = list(ROMAN_LINE.finditer(text))
    sections, was_short = [], False

    min_chars = 300

    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        is_short = len(body.strip()) < min_chars

        if not is_short and not was_short:
            body = SUBTITLE.sub("", PART_LINE.sub("", body))
            sections.append(" ".join(body.split()))
        was_short = is_short

    return sections


def tokenize(list_sections):

    list_lower = [section.lower() for section in list_sections]
    clean_lists = [re.sub(r'[^\w\s]', '', section) for section in list_lower]
    clean_text = [list.split(' ') for list in clean_lists]

    return clean_text


def remove_stopwords_stemming(words):

    stop_words = set(stopwords.words('english'))
    words_filtered = [word for word in words if word not in stop_words]

    stemmer = PorterStemmer()
    words_stemmed = [stemmer.stem(word) for word in words_filtered]

    return words_stemmed


# split Notes from the Underground at the start and end
u_start = "*** START OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"
u_end = "*** END OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"

underground_sections = tokenize(split_by_roman_numerals(clean_ebook_start_end(u_path, u_start, u_end)))
underground_processed = [remove_stopwords_stemming(section) for section in underground_sections]

# doing the same for Metamorphosis
m_start = "*** START OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"
m_end = "*** END OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"

metamorphosis_sections = tokenize(split_by_roman_numerals(clean_ebook_start_end(m_path, m_start, m_end)))
metamorphosis_processed = [remove_stopwords_stemming(section) for section in metamorphosis_sections]


"""
for section in underground_processed + metamorphosis_processed:
    print(section[:20])

# convert to dataframe
underground_df = pd.DataFrame(underground_processed)
metamorphosis_df = pd.DataFrame(metamorphosis_processed)

# save to project directory
underground_df.to_csv("underground.csv", index=False)
metamorphosis_df.to_csv("metamorphosis.csv", index=False)
"""
