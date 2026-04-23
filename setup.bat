@echo off
set VENV_DIR=venv
set SCRIPT_NAME=Start.py

echo Initializing...


:: 1. Create venv if missing
if not exist "%VENV_DIR%" (
    echo Configuring new environment...
    python -m venv %VENV_DIR%
)

:: 2. Activate the virtual environment
:: On Windows, the path is Scripts\activate instead of bin/activate
echo Activating...
call %VENV_DIR%\Scripts\activate.bat

:: 3. Force install/update PyYAML
:: Use python -m pip to ensure it installs into the active venv
echo Installing tools...

python -m pip install --disable-pip-version-check -q phonenumbers
python -m pip install --disable-pip-version-check -q boto3
python -m pip install --disable-pip-version-check -q pyyaml
python -m pip install --disable-pip-version-check -q psutil
python -m pip install --disable-pip-version-check -q cryptography
python -m pip install --disable-pip-version-check -q lxml
python -m pip install --disable-pip-version-check -q requests
python -m pip install --disable-pip-version-check -q httpx
python -m pip install --disable-pip-version-check -q bs4
echo Verify tools...
:: 4. Verification Step: Ensure 'deps' is actually importable


python -c "import bs4" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install bs4
)
python -c "import phonenumbers" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install phonenumbers
)

python -c "import boto3" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install boto3
)

python -c "import httpx" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install httpx
)
python -c "import yaml" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install pyyaml
)
python -c "import requests" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install requests
)

python -c "import psutil" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install psutil
)

python -c "import cryptography" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install cryptography
)

python -c "import lxml" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies. Retrying...
    python -m pip install lxml
)

:: 5. Run the script
:: %* passes all command line arguments to the python script
echo Launch Tool...
python %SCRIPT_NAME% %*

:: 6. Clean up
echo Deactivate...
call %VENV_DIR%\Scripts\deactivate

