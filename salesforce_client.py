import os
import requests
from dotenv import load_dotenv
from oauth_flow import refresh_salesforce_token, update_env_var

load_dotenv()

# def update_env_var(key, value):
#     """Overwrites or adds a key=value pair in .env cleanly."""
#     env_path = Path(".env")

#     # Load all lines safely
#     if env_path.exists():
#         with env_path.open("r") as f:
#             lines = f.readlines()
#     else:
#         lines = []

#     key_found = False
#     new_lines = []
#     for line in lines:
#         if line.strip().startswith(f"{key}="):
#             new_lines.append(f"{key}={value}\n")
#             key_found = True
#         else:
#             new_lines.append(line)

#     if not key_found:
#         new_lines.append(f"{key}={value}\n")

#     with env_path.open("w") as f:
#         f.writelines(new_lines)

#     # Also update in-memory environment immediately
#     os.environ[key] = value


def get_env_token():
    return os.getenv("SF_ACCESS_TOKEN")

def salesforce_request(method, endpoint, **kwargs):
    instance_url = os.getenv("SF_INSTANCE_URL")
    access_token = get_env_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{instance_url}{endpoint}"

    response = requests.request(method, url, headers=headers, **kwargs)

    # Handle expired token
    if response.status_code == 401:
        print("Token expired, attempting to refresh...")

        new_token = refresh_salesforce_token()
        if not new_token:
            print("Token refresh failed. Please reconnect via /.")
            return response  # return old failed response

        # Update in-memory and env variable
        if new_token:
            update_env_var("SF_ACCESS_TOKEN", new_token)
            headers["Authorization"] = f"Bearer {new_token}"

        # Retry the request with new token
        headers["Authorization"] = f"Bearer {new_token}"
        print("Retrying with refreshed token...")
        response = requests.request(method, url, headers=headers, **kwargs)

    return response
