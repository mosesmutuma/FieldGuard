#!/bin/bash
echo "==> Starting Vercel Build Process"

# Install requirements
python3 -m pip install -r requirements.txt

# Collect static files safely without interactive prompts
python3 manage.py collectstatic --noinput --clear

echo "==> Build Completed Successfully"