# Cloud Connexa Log Collection

**Date created** | 11/20/2024

**Last updated** | 11/27/2024

## Author and Contributors

**Author** | Gianni DePaola

**Contributor** | Nick Biacsi (Slof)

## Script Functionality

### Why was it written?
The purpose of this script is to pull logs from Cloud Connexa via its REST API so that the Elastic Agent can forward the logs to the SIEM.

SwaggerUI for CC API: https://uhm.api.openvpn.com/docs/swagger-ui

### What does it do?
**cc_log_collection.py**: Generates an Oauth token from Cloud Connexa for authentication, collects all session logs from Cloud Connexa from the last 15 minutes and write them to a timestamped log file.

**cc_log_cleanup.py**: Cleans up any log files that are over a day old.

Bash scripts are wrappers to run the python scripts in virtual environments from the crontab.

### Requirements
A valid Cloud Connexa API Client Secret and Client ID is required to authenticate to the API.

- These modules used are part of the standard python library: base64, json, datetime (datetime, timezone, timedelta)
- Install requirements.txt for the following required modules: requests, cryptography.fernet (fernet)

### Deployment Instructions
1. Install Python, python3-pip, and python3-venv on the server (ex: `apt install python3-pip`)
2. Clone repo to a folder (Git is required to do this: `apt install git`; `git clone <repo url>`).
3. Create virtual environment in the repo directory: `python3 -m venv venv`
    - Activate the virtual environment: `source venv/bin/activate`
    - Install the requirements: `pip install -r requirements.txt`
    - Deactivate the virtual environment: `deactivate`
3. Encrypt API keys to a '/keys' directory within the repo folder using 'encrypt_secret.py'.
4. Set up directory for log files (ex: `mkdir /opt/cc_logs`)
5. Point file paths in scripts towards the log file directory.
    - In cc_log_collection.py the variable for the path is "output_file"
    - In cc_log_cleanup.py the variable for the path is "logs_directory"
6. Set up cron jobs to run the run_cc_log_cleanup.sh script daily and the run_cc_log_collection.sh script every 15 minutes.