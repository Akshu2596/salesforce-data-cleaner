from pathlib import Path
from flask import Flask, render_template, request, redirect, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Read values from .env
CLIENT_ID = os.getenv("SF_CLIENT_ID")
CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SF_REDIRECT_URI")
AUTH_URL = os.getenv("SF_AUTH_URL")
TOKEN_URL = os.getenv("SF_TOKEN_URL")
ACCESS_TOKEN = os.getenv("SF_ACCESS_TOKEN")
INSTANCE_URL = os.getenv("SF_INSTANCE_URL")

@app.route("/")
def home():
    # Generate Salesforce login URL dynamically
    auth_link = (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return render_template("index.html", auth_link=auth_link)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code returned by Salesforce", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=data)
    result = response.json()

    if "error" in result:
        return jsonify(result), 400

    access_token = result.get("access_token")
    refresh_token = result.get("refresh_token")
    print("refresh_token: ",refresh_token)
    instance_url = result.get("instance_url")

    if access_token:
        update_env_var("SF_ACCESS_TOKEN", access_token)
        os.environ["SF_ACCESS_TOKEN"] = access_token

    if refresh_token:
        update_env_var("SF_REFRESH_TOKEN", refresh_token)
        os.environ["SF_REFRESH_TOKEN"] = refresh_token

    if instance_url:
        update_env_var("SF_INSTANCE_URL", instance_url)
        os.environ["SF_INSTANCE_URL"] = instance_url

    print("✅ Tokens successfully saved to .env")

    return jsonify({
        "message": "Access Token saved! You can close this tab.",
        "access_token": access_token,
        "instance_url": instance_url,
        "refresh_token": refresh_token
    })

def refresh_salesforce_token():
    refresh_token = os.getenv("SF_REFRESH_TOKEN")
    client_id = os.getenv("SF_CLIENT_ID")
    client_secret = os.getenv("SF_CLIENT_SECRET")
    token_url = "https://login.salesforce.com/services/oauth2/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        new_data = response.json()
        access_token = new_data.get("access_token")

        if access_token:
            update_env_var("SF_ACCESS_TOKEN", access_token)
            os.environ["SF_ACCESS_TOKEN"] = access_token
            print("✅ Salesforce token refreshed successfully.")
            return access_token

    else:
        print(f"❌ Failed to refresh token: {response.text}")
        return None
    
def update_env_var(key, value):
    """Overwrites or adds a key=value pair in .env cleanly."""
    env_path = Path(".env")

    # Load all lines safely
    if env_path.exists():
        with env_path.open("r") as f:
            lines = f.readlines()
    else:
        lines = []

    key_found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)

    if not key_found:
        new_lines.append(f"{key}={value}\n")

    with env_path.open("w") as f:
        f.writelines(new_lines)

    # Also update in-memory environment immediately
    os.environ[key] = value

if __name__ == "__main__":
    app.run(port=8080, debug=True)
