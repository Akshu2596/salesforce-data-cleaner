import re
import validators
from urllib.parse import urlparse

PHONE_RE = re.compile(r'\D+')

def normalize_phone(phone):
    """Normalize phone number and keep country code if present."""
    if not phone:
        return ''
    digits = PHONE_RE.sub('', phone)
    # Handle Indian numbers
    if len(digits) == 10:
        digits = '+91' + digits
    elif len(digits) > 10 and not digits.startswith('+'):
        digits = '+' + digits
    return digits


def normalize_website(website):
    """Ensure valid https:// URL, lowercased."""
    if not website:
        return ''
    website = website.strip().lower()
    if not website.startswith('http'):
        website = 'https://' + website

    # Parse + validate domain
    parsed = urlparse(website)
    if not parsed.netloc:
        return ''
    if not validators.url(website):
        return ''
    return website


def title_case_name(name):
    """Clean and title-case Name field."""
    if not name:
        return ''
    return ' '.join(word.capitalize() for word in name.strip().split())


def clean_record(rec):
    """Clean a single record with Salesforce-compatible normalization."""
    cleaned = {
        "Name": title_case_name(rec.get("Name") or rec.get("name") or ""),
        "Phone": normalize_phone(rec.get("Phone") or rec.get("phone") or ""),
        "Website": normalize_website(rec.get("Website") or rec.get("website") or "")
    }

    # Optional extra validations
    if len(cleaned["Name"]) > 255:
        cleaned["Name"] = cleaned["Name"][:255]

    return cleaned


def clean_data(records):
    """Clean list of records, remove duplicates, skip invalid."""
    cleaned = []
    seen = set()

    for rec in records:
        c = clean_record(rec)

        # Skip if Name is empty (Salesforce Account requires Name)
        if not c["Name"]:
            continue

        # Deduplicate based on normalized name
        key = c["Name"].lower()
        if key in seen:
            continue

        seen.add(key)
        cleaned.append(c)

    return cleaned
