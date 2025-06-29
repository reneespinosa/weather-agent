#!/bin/bash

# --- Weather Agent Runner ---
# This script automates the setup and execution of the Weather Agent.
# It ensures a clean environment and that all dependencies are met.

# Stop on first error to prevent unexpected behavior
set -e

# --- 1. Define Virtual Environment Directory ---
VENV_DIR="venv"

# --- 2. Create Virtual Environment if it doesn't exist ---
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in '$VENV_DIR'..."
    # Use python3 to create the virtual environment
    python3 -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# --- 3. Activate Virtual Environment & Install Dependencies ---
echo "Activating virtual environment..."
# The 'source' command loads the environment variables into the current shell
source $VENV_DIR/bin/activate

echo "Installing/updating dependencies from requirements.txt..."
# Use pip from the virtual environment to install packages
pip install --upgrade pip > /dev/null 2>&1 # Upgrade pip silently
pip install -r requirements.txt

echo ""
echo "--- Setup complete! ---"

# --- 4. Run the Application ---
echo "Starting Weather Agent..."
echo "The application should open in your browser at http://localhost:8000"
echo "Press Ctrl+C in this terminal to stop the server."
echo ""

# Execute the main Python script
python main.py

# The script will end here when the user stops main.py with Ctrl+C
echo ""
echo "Weather Agent stopped."

# Deactivate the environment (good practice)
deactivate
