import requests
import base64
import json
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

base_url = "https://uhm.api.openvpn.com/api/beta"

# Fernet Encryption variables and functions.
keys_folder_path: str = r"/opt/siem_logging_cloudconnexa/keys"
def get_secret_key(fnt: Fernet) -> str:
    contents: str = open(fr"{keys_folder_path}/secret_key.txt").read()
    return fnt.decrypt(contents).decode()

def get_access_key(fnt: Fernet) -> str:
    contents: str = open(fr"{keys_folder_path}/access_key.txt").read()
    return fnt.decrypt(contents).decode()

def get_decryption_key() -> str:
    return open(fr"{keys_folder_path}/key.key").read()

# Use encrypt_secret.py to store the API keys as encrypted text files
def get_cloudconnexa_token() -> str:
    '''
    Gets an access token from CloudConnexa that is used in all other CloudConnexa API calls.

    Returns:
        access_token (str): Access token from CloudConnexa API.
    '''

    # Grab keys via Fernet decryption
    fnt: Fernet = Fernet(get_decryption_key())
    access_key: str = get_access_key(fnt)
    secret_access_key: str = get_secret_key(fnt)

    if not access_key or not secret_access_key:
        raise ValueError("Encrypted values CLOUDCONNEXA_CLIENTID and CLOUDCONNEXA_CLIENTSECRET are not set.")

    str_bytes = f'{access_key}:{secret_access_key}'.encode('ascii')
    base64_bytes = base64.b64encode(str_bytes)
    base64_str = base64_bytes.decode('ascii')

    headers = {'Authorization': f'Basic {base64_str}'}
    url = base_url + '/oauth/token'

    response = requests.post(url=url, headers=headers)

    # Log the raw response details for debugging
    #print(f"Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch token: {response.status_code} {response.text}")

    return response.json().get('access_token', None)

def get_sessions_json(headers, start_date, output_file):
    next_cursor = None
    url = base_url + "/sessions"

    while True:
        # Include required parameters
        params = {
            "from": start_date,
            "size": 100,
        }
        if next_cursor:
            params["cursor"] = next_cursor 

        # Make the API request
        response = requests.get(url=url, headers=headers, params=params)

        # Check for successful response
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        # Parse JSON response
        data = response.json()
        
        with open(output_file, "a") as file:
            for session in data["sessions"]:
                json.dump(session, file)
                file.write("\n")

        # Check for the next cursor for pagination
        next_cursor = data.get("nextCursor")
        if not next_cursor:
            break



def main():
    # Token for authentication headers
    token = get_cloudconnexa_token()

    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    now = datetime.now(timezone.utc)
    start_time = (now - timedelta(minutes=15)).isoformat() + "Z"

    # Timestamp for file name in string format
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    #TODO: Write session logs to a JSON file - change file path in PROD
    output_file = f"/opt/cc_logs/session_logs_{timestamp}.log"

    # Pull logs from API and write to log file.
    get_sessions_json(headers, start_time, output_file)

    print(f"Session logs written to {output_file}")


if __name__ == "__main__":
    main()