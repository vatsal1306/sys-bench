#!/bin/bash
set -e

echo "Initializing System Benchmark..."

# Ensure the /data directory is writable
if [ ! -w "/data" ]; then
    echo "⚠️ WARNING: /data is not writable. Disk benchmark might fail. Please make it writable by command 'chmod 777 /data' or by mounting a writable volume."
fi

# Execute the Python benchmark
# We pass /data as an argument to tell the script where to write logs/temp files
exec python3 src/main.py /data