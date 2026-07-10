import re

def clean_text(text):
    if not text:
        return ""
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()

def extract_dates(text):
    if not text:
        return (None, None)
    match = re.search(r'(\w+ \d{4})\s*[-–]\s*(\w+ \d{4}|Present)', text)
    if match:
        return match.groups()
    match_year = re.search(r'(\d{4})', text)
    if match_year:
        return (match_year.group(1), None)
    return (None, None)
