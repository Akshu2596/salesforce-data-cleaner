import os
import requests
from oauth_flow import refresh_salesforce_token
from salesforce_client import salesforce_request

def upload_to_salesforce(records):
    access_token = os.getenv("SF_ACCESS_TOKEN")
    instance_url = os.getenv("SF_INSTANCE_URL")
    url = f"{instance_url}/services/data/v61.0/sobjects/Account"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    for record in records:
        response = salesforce_request(
                    "POST",
                    "/services/data/v60.0/sobjects/Account/",
                    json=record
        )
        # response = requests.post(url, json=record, headers=headers)

        if response.status_code == 401:  # Unauthorized (expired token)
            print("Token expired, refreshing...")
            new_token = refresh_salesforce_token()
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                response = requests.post(url, json=record, headers=headers)
            else:
                return {"status": "error", "message": "Failed to refresh token."}

        if response.status_code not in (200, 201, 204):
            print(f"Failed to insert record: {response.text}")
            return {"status": "error", "message": response.text}

    print("All records uploaded successfully!")
    return {"status": "success", "message": "Records uploaded to Salesforce."}
