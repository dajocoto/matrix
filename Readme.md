🚀 Matrix Style Console

A lightweight, self-initializing Python console application that automatically prepares its environment, installs dependencies, and launches with a single command.

📌 Overview

This project is designed for simplicity and portability. On startup, the application:

Checks for a local Python virtual environment
Creates one if it doesn't exist
Installs all required dependencies
Verifies installations
Launches the main application script

No manual setup required.

⚙️ Features

✅ Automatic virtual environment setup (venv)

📦 Dependency auto-installation and verification

🔁 Retry mechanism for failed installs

🖥️ Cross-platform launch support (Windows & macOS)

🚀 One-command startup

📂 Project Structure


├── Start.py            # Main application entry point

├── venv/               # Auto-generated virtual environment

├── setup.bat           # Windows launcher

├── setup.sh            # macOS/Linux launcher

└── README.md
🔧 Requirements
Python 3.8+
Internet connection (for dependency installation)
📦 Dependencies

The following Python packages are automatically installed:

phonenumbers
boto3
pyyaml
psutil
cryptography
lxml
requests
httpx
beautifulsoup4 (bs4)
▶️ Getting Started

🪟 Windows

Run the provided batch script:

setup.bat


🍎 macOS / 🐧 Linux

Make the script executable (first time only):

chmod +x setup.sh

Then run:

./setup.sh



<img width="1651" height="922" alt="image" src="https://github.com/user-attachments/assets/a2b0755f-2b74-4f1a-bd21-39f38bf234e1" />


🔄 How It Works

The launcher script performs the following steps:

Environment Setup
Checks for /venv
Creates it if missing using python -m venv
Activation
Activates the virtual environment
Dependency Installation
Installs required packages silently
Uses python -m pip to ensure correct environment targeting
Verification
Attempts to import each dependency
Retries installation if any module fails
Execution

Runs:

python setup.py
Cleanup
Deactivates the virtual environment after execution
🧪 Passing Arguments

You can pass arguments directly through the launcher:

setup.bat arg1 arg2

or

./setup.sh arg1 arg2

These will be forwarded to setup.py.

⚠️ Notes
The virtual environment is created locally and not committed to version control.
If you encounter persistent dependency issues, try deleting the venv/ folder and restarting.
Ensure python is available in your system PATH.
🛠️ Customization

To modify dependencies, edit the install section in the launcher script.

To change the entry point, update:

set SCRIPT_NAME=setup.py
