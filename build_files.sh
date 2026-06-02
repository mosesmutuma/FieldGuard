#!/bin/bash

echo "==> Starting Vercel Build Process"

# Install your dependencies using the flag required by Vercel's newer python image
pip install -r requirements.txt --break-system-packages

# Run your static collection rules directly from the root
python3 manage.py collectstatic --noinput

echo "==> Build Completed Successfully"