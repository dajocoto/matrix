#!/bin/bash

# Define paths
VENV_DIR="venv"
SCRIPT_NAME="Start.py"

echo "--- Initializing Apps Distributor ---"

# 1. Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Configuring new Python environment..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Activate
source "$VENV_DIR/bin/activate"

# 3. Force install/update PyYAML
# We use --disable-pip-version-check to keep the output clean
pip install --disable-pip-version-check -q bs4
pip install --disable-pip-version-check -q phonenumbers
pip install --disable-pip-version-check -q boto3
pip install --disable-pip-version-check -q pyyaml
pip install --disable-pip-version-check -q psutil
pip install --disable-pip-version-check -q cryptography
pip install --disable-pip-version-check -q lxml
pip install --disable-pip-version-check -q requests
pip install --disable-pip-version-check -q httpx
# 4. Verification Step: Ensure 'yaml' is actually importable

if ! python3 -c "import bs4" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install bs4
fi
if ! python3 -c "import phonenumbers" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install phonenumbers
fi

if ! python3 -c "import httpx" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install httpx
fi

if ! python3 -c "import boto3" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install boto3
fi

if ! python3 -c "import requests" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install requests
fi

if ! python3 -c "import yaml" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install pyyaml
fi

if ! python3 -c "import psutil" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install psutil
fi
if ! python3 -c "import cryptography" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install cryptography
fi
if ! python3 -c "import lxml" &> /dev/null; then
    echo "Error: Failed to install dependencies. Retrying..."
    pip install lxml
fi
# 5. Run the script
python3 "$SCRIPT_NAME" "$@"

# 6. Clean up
deactivate