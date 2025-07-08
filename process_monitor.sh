#!/bin/bash

# --- Configuration ---
PROCESS_NAME="log_analyzer.py"
PYTHON_COMMAND="python3"
LOG_FILE_PATH="/home/ec2-user/process_monitor.log" # Log file for the monitor itself
PROJECT_DIR="/home/ec2-user/aws-log-analyzer-sre-project" # Absolute path to your project

# --- Script Logic ---

# Get the current timestamp for logging
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Check if the process is running
# pgrep -f looks for the full command line string
if pgrep -f "$PROCESS_NAME" > /dev/null
then
    # If it's running, do nothing and log it.
    echo "[$TIMESTAMP] - STATUS: Process '$PROCESS_NAME' is running." >> "$LOG_FILE_PATH"
else
    # If it's not running, log the event and restart it.
    echo "[$TIMESTAMP] - ALERT: Process '$PROCESS_NAME' was not found." >> "$LOG_FILE_PATH"
    echo "[$TIMESTAMP] - ACTION: Attempting to restart the process..." >> "$LOG_FILE_PATH"

    # Go to the project directory and restart the process in the background
    # nohup allows the script to keep running even if you close the terminal
    # & runs the command in the background
    # > /dev/null 2>&1 redirects all output (stdout and stderr) to nowhere, so it doesn't clutter the terminal
    cd "$PROJECT_DIR" && nohup $PYTHON_COMMAND $PROCESS_NAME > /dev/null 2>&1 &
    
    # Check if the restart was successful
    if pgrep -f "$PROCESS_NAME" > /dev/null
    then
        echo "[$TIMESTAMP] - SUCCESS: Process '$PROCESS_NAME' has been restarted." >> "$LOG_FILE_PATH"
    else
        echo "[$TIMESTAMP] - FAILURE: Failed to restart the process '$PROCESS_NAME'." >> "$LOG_FILE_PATH"
    fi
fi