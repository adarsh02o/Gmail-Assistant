#!/bin/bash
# Enable logging for debugging
exec >> "/home/zen/openclaw gmail /cron_debug.log" 2>&1
echo "Starting Gmail Automator at $(date)"

cd "/home/zen/openclaw gmail " || { echo "Failed to cd to directory"; exit 1; }  

# Execute the python script
if "/home/zen/openclaw gmail /.venv/bin/python" gmail_automator.py; then
    echo "Gmail Automator finished successfully at $(date)"
else
    echo "Gmail Automator failed with exit code $? at $(date)"
    exit 1
fi
