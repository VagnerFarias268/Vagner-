#!/bin/bash
# Convenient wrapper script - can be run from anywhere

# Get the script's directory (project root)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

# Activate venv
source venv/bin/activate

# Run the application
python3 run.py
