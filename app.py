import os
import re
import json
from flask import Flask, request, jsonify
from datetime import datetime
from salesforce_api import upload_to_salesforce
from flask_cors import CORS

app = Flask(__name__)
#enable CORS
CORS(app)

def clean_name(name: str) -> str:
    return name.strip().title()

def clean_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)  # remove non-digits
    if len(digits) == 10:
        digits = "91" + digits
    elif digits.startswith("0") and len(digits) == 11:
        digits = "91" + digits[1:]
    return f"+{digits}"

def clean_website(website: str) -> str:
    site = website.strip().lower()
    if not site.startswith("http"):
        site = "https://" + site
    return site

def clean_record(record: dict) -> dict:
    return {
        "Name": clean_name(record.get("Name", "")),
        "Phone": clean_phone(record.get("Phone", "")),
        "Website": clean_website(record.get("Website", "")),
    }

@app.route("/clean_and_upload", methods=["POST"])
def clean_and_upload():
    try:
        data = request.get_json()

        if not data or "records" not in data:
            return jsonify({"status": "error", "message": "JSON must include 'records'."}), 400

        raw_records = data["records"]
        valid_records = []
        invalid_records = []

        for r in raw_records:
            cleaned = clean_record(r)
            # If Name missing, mark invalid
            if not cleaned.get("Name"):
                invalid_records.append(r)
                continue
            valid_records.append(cleaned)

        # Save locally
        cleaned_folder = "cleaned"
        os.makedirs(cleaned_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        cleaned_path = os.path.join(cleaned_folder, f"cleaned_{timestamp}.json")

        with open(cleaned_path, "w") as f:
            json.dump(valid_records, f, indent=2)

        # Upload to Salesforce
        upload_result = upload_to_salesforce(valid_records)

        return jsonify({
            "status": "success",
            "message": "Data cleaned successfully",
            "saved_to": cleaned_path,
            "total_records": len(raw_records),
            "valid_records": len(valid_records),
            "invalid_records": len(invalid_records),
            "invalid_samples": invalid_records[:3]
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
