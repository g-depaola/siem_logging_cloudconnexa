import os
from datetime import datetime, timezone

def clean_up_logs(directory, days_old=1, error_log_file="cleanup_errors.log"):
    """
    Deletes log files in the specified directory that are older than a given number of days in UTC.
    
    Args:
        directory (str): Path to the directory containing log files.
        days_old (int): Number of days after which files should be deleted. Default is 1 day.
        error_log_file (str): File where errors will be logged. Default is 'cleanup_errors.log'.
    """
    # Calculate the cutoff time in UTC
    now_utc = datetime.now(timezone.utc)
    cutoff_time = now_utc.timestamp() - (days_old * 86400)  # Convert days to seconds

    # Ensure the directory exists
    if not os.path.exists(directory):
        with open(error_log_file, "a") as log_file:
            log_file.write(f"[{now_utc.isoformat()}] Directory {directory} does not exist.\n")
        return

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip if it's not a file
        if not os.path.isfile(file_path):
            continue

        # Check file's last modified time in UTC
        file_last_modified = os.path.getmtime(file_path)

        # Delete the file if it is older than the cutoff time
        if file_last_modified < cutoff_time:
            try:
                os.remove(file_path)
                print(f"Deleted old log file: {filename}")
            except Exception as e:
                # Log the error to the error log file
                with open(error_log_file, "a") as log_file:
                    log_file.write(f"[{now_utc.isoformat()}] Error deleting file {filename}: {e}\n")

if __name__ == "__main__":
    # Specify the directory containing log files
    logs_directory = "/opt/cc_logs"  # Adjust to your logs directory
    clean_up_logs(logs_directory, days_old=1)
