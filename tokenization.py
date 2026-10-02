from pathlib import Path
from itertools import islice
import re


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
    
    # drop any text before Roman Numeral I
    parts = re.split(r'(?:^|\n)[ \t]*I[ \t]*(?:\n|$)', text, maxsplit=1)

    if len(parts) < 2:
        return []

    content = parts[1]
    
    # regex for splitting remaining text by Roman Numerals II-X
    pattern = r'(?:\n|^)[ \t]*(?:X|IX|VIII|VII|VI|V|IV|III|II)[ \t]*(?:\n|$)'

    # split and remove empty strings and newlines
    sections = [section.strip() for section in re.split(pattern, content)]
    sections_without_newlines = [section.replace("\n", " ") for section in sections]
    return [s for s in sections_without_newlines if s]

# split Notes from the Underground at the start and end
u_start = "*** START OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"
u_end = "*** END OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"

underground = clean_ebook_start_end(u_path, u_start, u_end)

# split into sections
underground_sections = split_by_roman_numerals(underground)

for s in underground_sections:
    print(s[:50])


# doing the same for Metamorphosis
m_start = "*** START OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"
m_end = "*** END OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"

metamorphosis = clean_ebook_start_end(m_path, m_start, m_end)


