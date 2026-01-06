import re
import unicodedata

def normalize_text(text: str) -> str:
  if not text:
    return ""

  # Normalize unicode (é → e)
  text = unicodedata.normalize("NFKD", text)

  # Lowercase
  text = text.lower()

  # Convert Persian digits to English
  text = fa_to_en_digits(text)

  # Remove special characters (keep letters, numbers, space)
  # Keep:
  # - English letters
  # - Persian letters
  # - Numbers
  # - Spaces
  text = re.sub(r"[^a-z0-9\u0600-\u06FF\u0750-\u077F\s]", "", text)

  # Remove extra spaces
  text = re.sub(r"\s+", " ", text).strip()

  return text

def extract_patterns(text: str) -> dict:
  clean_text = fa_to_en_digits(text)

  patterns = {
    "emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "dates": r"\b[۰-۹0-9]{4}[-/][۰-۹0-9]{2}[-/][۰-۹0-9]{2}\b",
    "urls": r"https?://[^\s]+",
  }

  extracted = {}
  for key, pattern in patterns.items():
    extracted[key] = remove_duplicates(re.findall(pattern, clean_text))

  return extracted

def split_and_clean(text: str, separator=",") -> list[str]:
  items = text.split(separator)
  return [normalize_text(item) for item in items if item.strip()]

def fa_to_en_digits(text: str) -> str:
  fa = "۰۱۲۳۴۵۶۷۸۹"
  en = "0123456789"
  return text.translate(str.maketrans(fa, en))

def remove_duplicates(values: list[str]) -> list[str]:
  return list(dict.fromkeys(values))

def clean_scraped_value(raw_value: str) -> dict:
  normalized = normalize_text(raw_value)

  return {
    "raw": raw_value,
    "normalized": normalized,
    "patterns": extract_patterns(raw_value),
    "tokens": split_and_clean(raw_value),
  }
