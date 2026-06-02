#!/bin/bash

echo "==> Starting Vercel Build Process"

# Check if manage.py is in the current directory or a subfolder, and navigate accordingly
if [ -f "manage.py" ]; then
    echo "Found manage.py in current directory."
    TARGET_DIR="."
elif [ -f "attendance/manage.py" ]; then
    echo "Found manage.py inside attendance subfolder. Navigating..."
    cd attendance
    TARGET_DIR="."
else
    echo "ERROR: manage.py could not be found anywhere!"
    exit 1
fi

# Install dependencies using the correct local paths
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --break-system-packages
else
    pip install -r ../requirements.txt --break-system-packages
fi

# Run static collection rules
python3 manage.py collectstatic --noinput

echo "==> Build Completed Successfully"