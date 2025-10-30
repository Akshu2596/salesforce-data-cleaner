import os
import requests
from dotenv import load_dotenv

load_dotenv()

SF_INSTANCE_URL = os.getenv("SF_INSTANCE_URL")
SF_ACCESS_TOKEN = os.getenv("SF_ACCESS_TOKEN")

def upload_to_salesforce(records):
    
    if not SF_INSTANCE_URL or not SF_ACCESS_TOKEN:
        raise ValueError("Salesforce environment variables not set.")

    url = f"{SF_INSTANCE_URL}/services/data/v61.0/sobjects/Account/"
    headers = {
        "Authorization": f"Bearer {SF_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    success, failed = [], []

    for rec in records:
        try:
            res = requests.post(url, headers=headers, json=rec)
            if res.status_code == 201:
                success.append(res.json())
            else:
                failed.append({
                    "record": rec,
                    "error": res.text
                })
        except Exception as e:
            failed.append({"record": rec, "error": str(e)})

    return {"success": success, "failed": failed}
