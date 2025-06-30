#!/bin/bash
set -e

# Ensure pip is up to date
python -m pip install --upgrade pip

# Install Python dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    python -m pip install -r requirements.txt
fi
