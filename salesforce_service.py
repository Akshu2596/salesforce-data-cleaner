import os
import json
import requests
from datetime import datetime

# If MOCK=true in env, we won't call Salesforce and instead write results to cleaned/ folder
MOCK = os.getenv("MOCK", "true").lower() in ("1","true","yes")

# Use SF_ACCESS_TOKEN + SF_INSTANCE_URL if provided
SF_ACCESS_TOKEN = os.getenv("SF_ACCESS_TOKEN")
SF_INSTANCE_URL = os.getenv("SF_INSTANCE_URL")  # e.g.: https://yourinstance.my.salesforce.com

API_VERSION = os.getenv("SF_API_VERSION", "64.0")

def _mock_write(records):
    out_path = os.path.join("cleaned", f"cleaned_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    results = [{"record": r.get("Name"), "status": "mocked", "id": None} for r in records]
    return {"mock_file": out_path, "details": results}

def _post_to_sobject(record):
    # single record via sobjects endpoint
    if not SF_ACCESS_TOKEN or not SF_INSTANCE_URL:
        raise RuntimeError("SF_ACCESS_TOKEN and SF_INSTANCE_URL must be set in the environment for non-mock mode.")
    headers = {
        "Authorization": f"Bearer {SF_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{SF_INSTANCE_URL}/services/data/v{API_VERSION}/sobjects/Account"
    resp = requests.post(url, json=record, headers=headers, timeout=30)
    try:
        return {"status_code": resp.status_code, "response": resp.json()}
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}

def push_to_salesforce(records):
    if MOCK:
        return _mock_write(records)

    results = []
    # For small data sets we call sobjects endpoint per record.
    for r in records:
        try:
            res = _post_to_sobject(r)
            results.append(res)
        except Exception as e:
            results.append({"error": str(e)})
    return results
