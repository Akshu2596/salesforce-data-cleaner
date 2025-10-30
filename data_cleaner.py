import re
from urllib.parse import urlparse

PHONE_RE = re.compile(r'\D+')

def normalize_phone(phone):
    if not phone:
        return ''
    # Remove non-digit characters
    digits = PHONE_RE.sub('', phone)
    # Basic normalization (no country inference)
    return digits

def normalize_website(website):
    if not website:
        return ''
    website = website.strip().lower()
    if website.startswith('http://') or website.startswith('https://'):
        return website
    # ensure at least a domain
    return 'https://' + website

def title_case_name(name):
    if not name:
        return ''
    return ' '.join([w.capitalize() for w in name.strip().split()])

def clean_record(rec):
    return {
        "Name": title_case_name(rec.get("Name") or rec.get("name") or ""),
        "Phone": normalize_phone(rec.get("Phone") or rec.get("phone") or ""),
        "Website": normalize_website(rec.get("Website") or rec.get("website") or "")
    }

def clean_data(records):
    cleaned = []
    seen = set()
    for rec in records:
        c = clean_record(rec)
        # Skip if Name is empty (Account requires Name)
        if not c["Name"]:
            continue
        # Deduplicate based on normalized name
        key = c["Name"].lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(c)
    return cleaned
