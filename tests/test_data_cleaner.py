from data_cleaner import clean_data

def test_clean_basic():
    raw = [
        {"Name":"  acme corp  ","Phone":"+91 98765 43210","Website":"WWW.Acme.COM"},
        {"Name":"ACME corp","Phone":"9876543210","Website":"acme.com"},
        {"Name":"", "Phone":"123","Website":""}
    ]
    cleaned = clean_data(raw)
    assert len(cleaned) == 1
    assert cleaned[0]["Name"] == "Acme Corp"
