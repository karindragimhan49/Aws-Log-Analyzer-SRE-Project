import boto3
import time

# --- Configuration ---
# !!! IMPORTANT: Replace with your actual S3 bucket name !!!
S3_BUCKET_NAME = "karindra-log-analyzer-project-20231027"
REGION_NAME = "us-east-2" # Ohio
LOG_PREFIX = "logs/" # The folder inside the bucket where logs are stored

# Initialize AWS clients
s3_client = boto3.client("s3", region_name=REGION_NAME)
cloudwatch_client = boto3.client("cloudwatch", region_name=REGION_NAME)

def process_log_file(bucket, key):
    """Reads a log file from S3, counts errors, and deletes the file."""
    print(f"Processing file: s3://{bucket}/{key}")
    
    try:
        # Get the log file content from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        log_content = response['Body'].read().decode('utf-8')
        
        lines = log_content.splitlines()
        error_count = 0
        
        # Count lines containing "ERROR" or "CRITICAL"
        for line in lines:
            if "ERROR" in line or "CRITICAL" in line:
                error_count += 1
                print(f"  - Found Error/Critical line: {line.strip()}")

        print(f"  - Total errors found in this file: {error_count}")
        
        # --- IMPORTANT: Send data to CloudWatch ---
        if error_count > 0:
            send_metric_to_cloudwatch('ErrorCount', error_count)

        # Delete the processed file from S3 to avoid re-processing
        s3_client.delete_object(Bucket=bucket, Key=key)
        print(f"  - Deleted processed file: {key}")

    except Exception as e:
        print(f"Error processing file {key}: {e}")

def send_metric_to_cloudwatch(metric_name, value):
    """Sends a custom metric to AWS CloudWatch."""
    try:
        cloudwatch_client.put_metric_data(
            Namespace='LogAnalyzerApp', # A custom namespace for our project
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': 'Count'
                },
            ]
        )
        print(f"Successfully sent metric '{metric_name}' with value {value} to CloudWatch.")
    except Exception as e:
        print(f"Error sending metric to CloudWatch: {e}")


if __name__ == "__main__":
    print("Log Analyzer Started. Looking for new logs...")
    while True:
        try:
            # List objects in the S3 bucket under the 'logs/' prefix
            response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=LOG_PREFIX)
            
            if 'Contents' in response:
                # Get the list of log files
                log_files = response['Contents']
                
                # Sort files by last modified time to process oldest first
                log_files.sort(key=lambda x: x['LastModified'])

                for log_file in log_files:
                    file_key = log_file['Key']
                    # Make sure we don't process the folder itself
                    if file_key.endswith(".log"):
                        process_log_file(S3_BUCKET_NAME, file_key)
            else:
                print("No new log files found. Waiting...")

            # Wait for some time before checking for new files again
            time.sleep(15) # Check every 15 seconds

        except KeyboardInterrupt:
            print("\nLog Analyzer Stopped.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(30) # Wait longer if there's an error