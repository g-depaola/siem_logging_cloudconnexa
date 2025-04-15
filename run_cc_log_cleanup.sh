#!/bin/bash
# Activate the virtual environment
source /opt/siem_logging_cloudconnexa/venv/bin/activate

# Run the Python script
python3 /opt/siem_logging_cloudconnexa/cc_log_cleanup.py

# Deactivate the virtual environment (optional, for clarity)
deactivate
