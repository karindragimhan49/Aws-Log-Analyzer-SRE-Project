import boto3
import datetime
import random
import time
import os

# --- Configuration ---
# !!! IMPORTANT: Replace with your actual S3 bucket name !!!
S3_BUCKET_NAME = "karindra-log-analyzer-project-20231027" 
REGION_NAME = "us-east-2"  # The region where your EC2 and S3 are (Ohio)
LOG_FILE_NAME = "application.log"

# --- Log Messages ---
LOG_LEVELS = ["INFO", "INFO", "INFO", "WARNING", "ERROR", "CRITICAL"]
SUCCESS_MESSAGES = [
    "User logged in successfully.",
    "Data processed without errors.",
    "API call to external service succeeded.",
    "File uploaded to repository.",
]
WARNING_MESSAGES = [
    "Disk space is running low.",
    "API response time is high.",
    "Memory usage is approaching threshold.",
]
ERROR_MESSAGES = [
    "Database connection failed.",
    "Failed to read configuration file.",
    "User authentication failed: Invalid credentials.",
    "Critical service is not responding.",
]

# Initialize the S3 client
# When running on EC2 with an IAM role, Boto3 automatically finds credentials.
s3_client = boto3.client("s3", region_name=REGION_NAME)

def generate_log_entry():
    """Creates a single line of a log entry."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(LOG_LEVELS)
    
    if log_level == "INFO":
        message = random.choice(SUCCESS_MESSAGES)
    elif log_level == "WARNING":
        message = random.choice(WARNING_MESSAGES)
    else: # ERROR or CRITICAL
        message = random.choice(ERROR_MESSAGES)
        
    return f"[{timestamp}] [{log_level}] - {message}\n"

def upload_log_to_s3(file_path, bucket, object_name):
    """Uploads a file to an S3 bucket."""
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        print(f"Successfully uploaded {file_path} to s3://{bucket}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    print("Log Generator Started. Press Ctrl+C to stop.")
    try:
        while True:
            # Generate a few log lines
            with open(LOG_FILE_NAME, "w") as f:
                num_lines = random.randint(5, 15)
                for _ in range(num_lines):
                    f.write(generate_log_entry())
            
            # Create a unique name for the S3 object based on timestamp
            s3_object_name = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
            
            # Upload the generated log file to S3
            upload_log_to_s3(LOG_FILE_NAME, S3_BUCKET_NAME, s3_object_name)
            
            # Clean up the local log file
            os.remove(LOG_FILE_NAME)
            
            # Wait for a short period before generating the next log file
            time.sleep(10) # Generate a new log file every 10 seconds

    except KeyboardInterrupt:
        print("\nLog Generator Stopped.")