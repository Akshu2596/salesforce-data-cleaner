# Salesforce Data Cleaner

A lightweight Flask microservice that **cleans, validates, and uploads data to Salesforce** using the REST API.  
It includes **OAuth2 authentication**, **automatic token refresh**, and **direct .env updates** — no more manual token handling!

---

## Overview

This project streamlines the process of preparing and uploading records to Salesforce.  
It cleans data (like names, phone numbers, and websites), validates them, and pushes them to your Salesforce org securely.

### Features

- OAuth2-based Salesforce connection
- Auto token refresh** (access token updated in `.env`)
- Data cleaning** (names, phones, websites)
- Handles invalid and missing records gracefully
- Saves cleaned records locally as JSON backups
- Built-in retry for expired tokens
- CORS-enabled Flask API for frontend integration

---

## Project Structure

salesforce-data-cleaner/
│
├── app.py # Flask app for cleaning + uploading data
├── oauth_flow.py # Handles OAuth2 login & token refresh
├── salesforce_api.py # Uploads records to Salesforce + refreshes token on expiry
│
├── templates/
│ └── index.html # Simple UI for connecting & uploading
│
├── cleaned/ # Saved cleaned files
├── .env # Stores Salesforce credentials and auto-updated tokens
├── requirements.txt # Python dependencies
└── README.md

⚙️ Setup Instructions

1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/salesforce-data-cleaner.git
cd salesforce-data-cleaner

2️⃣ Create a Virtual Environment
bash

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

3️⃣ Install Dependencies
bash

pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create a .env file with the following:

env

SF_CLIENT_ID=your_salesforce_client_id
SF_CLIENT_SECRET=your_salesforce_client_secret
SF_REDIRECT_URI=http://127.0.0.1:8080/callback
SF_AUTH_URL=https://login.salesforce.com/services/oauth2/authorize
SF_TOKEN_URL=https://login.salesforce.com/services/oauth2/token

# These will be auto-filled after first auth
SF_ACCESS_TOKEN=
SF_REFRESH_TOKEN=
SF_INSTANCE_URL=

▶️ How to Run

Step 1: Start the OAuth Service
Handles authentication & token refresh.

bash

python oauth_flow.py
Then visit
http://127.0.0.1:8080

Click “Connect to Salesforce”, authorise, and your .env will automatically update with fresh tokens and instance details.

Step 2: Start the Data Cleaner Service
Handles data upload and cleaning.

bash

python app.py
API will be available at
http://127.0.0.1:5000

You can POST data via the UI or API endpoint /clean_and_upload.

Data Cleaning Rules
Field	Cleaning Logic
Name	Removes quotes, trims spaces, converts to Title Case
Phone	Removes non-digit characters, formats as “+91XXXXXXXXXX”
Website	Ensures lowercase and adds “https://” prefix if missing

Example API Request:
POST /clean_and_upload

json

{
  "records": [
    { "Name": "\"Acme  Corp \"", "Phone": "(987)-654-3210", "Website": "acme.com" },
    { "Name": "   ", "Phone": "12345", "Website": "" }
  ]
}
Response:

json

{
  "status": "success",
  "message": "Data cleaned successfully",
  "total_records": 2,
  "valid_records": 1,
  "invalid_records": 1,
  "saved_to": "cleaned/cleaned_20251112123500.json"
}

Token Handling
If Salesforce returns 401 Unauthorised, the app automatically refreshes the token.

The .env file is updated instantly with the new SF_ACCESS_TOKEN.

No stale token issues or manual edits needed.

Tech Stack

Python 3.10+
Flask
Requests
Flask-CORS
python-dotenv
Salesforce REST API

Future Enhancements

Add support for Contacts and Leads
Deploy on Render/Heroku
Cleaning summary dashboard

Author
Aksh — Software Developer
Building clean, smart, and automated Salesforce data tools

