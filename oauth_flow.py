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
    # Get the "code" from the Salesforce redirect
    code = request.args.get("code")
    if not code:
        return "Error: No code returned by Salesforce", 400

    # Exchange the code for an access token
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

    # Save token (you can persist it to file/db)
    with open("token.json", "w") as f:
        f.write(response.text)

    return jsonify(result)

def refresh_salesforce_token():
    TOKEN_URL = os.getenv("SF_TOKEN_URL")
    CLIENT_ID = os.getenv("SF_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("SF_REFRESH_TOKEN")

    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }

    try:
        response = requests.post(TOKEN_URL, data=data)
        if response.status_code == 200:
            resp_json = response.json()
            new_token = resp_json["access_token"]
            print("Token refreshed successfully!")
            
            # Store in env (runtime memory only)
            os.environ["SF_ACCESS_TOKEN"] = new_token
            
            # Optionally write to .env file
            env_path = ".env"
            with open(env_path, "r") as f:
                lines = f.readlines()
            with open(env_path, "w") as f:
                for line in lines:
                    if line.startswith("SF_ACCESS_TOKEN="):
                        f.write(f"SF_ACCESS_TOKEN={new_token}\n")
                    else:
                        f.write(line)
            print("Updated .env with new access token.")
            
            return new_token
        else:
            print(f"Failed to refresh token: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Exception during token refresh: {e}")
        return None





if __name__ == "__main__":
    app.run(port=8080, debug=True)
