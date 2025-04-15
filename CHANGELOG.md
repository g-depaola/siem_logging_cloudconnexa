# Changelog
Please follow best practices for updating the changelog.
- Reference a DevOps card, ticket or request number, or commit for each line item.
- Include an author name after each reference.

## VERSION - DATE (1.1.2 - 11/27/2024)

### Fixed
- Fixed Issue 2

### New Feature
- Removed json dumping from the main() script and added the functionality to the get_sessions_json function. (gdepaola)
    - Added an additional parameter for the output file path to the get_sessions_json function. (gdepaola)
    - Function no longer returns a value and instead handles pulling the logs and appending them to a log file. (gdepaola)
    - Used a for each loop to write each session in sessions to a new line. (nbiacsi)
        - This removed the need for a return statement and for the all_logs list.
- Removed the 'os' library as it is no longer used. (gdepaola)

### Known Issues
- None

## VERSION - DATE (1.1.0 - 11/25/2024)

### Fixed
- Fixed Issue 1

### New Feature
- Replaced storing API keys as environment variables with Fernet encryption instead. (gdepaola)
    - Store the decryption key and text files with encrypted secrets in a '/keys' directory within the repo folder.
    - Use the 'encrypt_secret.py' script to generate the key and encrypt the secrets. (nbiacsi)
- Scripts will now run within a virtual environment on the server. Introduced bash scripts to assist with this. (gdepaola)
    - [run_cc_log_collection.sh] A wrapper script written in bash will execute from the crontab to initialize the virtual environment, run the log collection script, then deactivate.
    - [run_cc_log_cleanup.sh] A wrapper script written in bash will execute from the crontab to initialize the virtual environment, run the log cleanup script, then deactivate.
- Updated .gitignore to prevent test keys and test scripts from being committed to repo. (gdepaola)
- Added requirements.txt for the cryptography and requests libraries.
- Updated README with clearer deployment instructions.

### Known Issues
- [Issue 2] JSON not being parsed correctly because of indentation

## VERSION - DATE (1.0.0 - 11/21/2024)

### Fixed
- None

### New Feature
- Initial commit

### Known Issues
- [Issue 1] Ubuntu crontab having issues reading the environment variables.