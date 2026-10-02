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



# split Notes from the Underground at the start and end
u_start = "*** START OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"
u_end = "*** END OF THE PROJECT GUTENBERG EBOOK NOTES FROM THE UNDERGROUND ***"

underground_sections = tokenize(split_by_roman_numerals(clean_ebook_start_end(u_path, u_start, u_end)))

# doing the same for Metamorphosis
m_start = "*** START OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"
m_end = "*** END OF THE PROJECT GUTENBERG EBOOK METAMORPHOSIS ***"

metamorphosis_sections = tokenize(split_by_roman_numerals(clean_ebook_start_end(m_path, m_start, m_end)))
