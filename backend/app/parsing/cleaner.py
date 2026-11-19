import re
import unicodedata

BULLET_CHARS = "•●▪■◦‣∙➢➤►✓✔"


def normalize_unicode(text):
    return unicodedata.normalize("NFKC", text)


def remove_invisible_chars(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]", "", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text


def fix_hyphenation(text):
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def standardize_bullets(text):
    pattern = "[" + re.escape(BULLET_CHARS) + "]"
    return re.sub(pattern, "- ", text)


def collapse_whitespace(text):
    text = re.sub(r"[ \t]+", " ", text)
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text(text):
    if not text:
        return ""

    text = normalize_unicode(text)
    text = remove_invisible_chars(text)
    text = fix_hyphenation(text)
    text = standardize_bullets(text)
    text = collapse_whitespace(text)
    return text