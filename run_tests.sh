#!/bin/bash

# Bash script to run the test suite for Pink Morsel Sales Dashboard
# This script activates the virtual environment and runs pytest
# Returns exit code 0 if all tests pass, 1 if any test fails

set -e  # Exit on any error

echo "================================"
echo "Pink Morsel Sales Dashboard Tests"
echo "================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate the virtual environment
echo "Activating virtual environment..."
if [ -d "venv/Scripts" ]; then
    # Windows Git Bash or WSL style
    source venv/Scripts/activate
elif [ -d "venv/bin" ]; then
    # Unix/Linux/Mac style
    source venv/bin/activate
else
    echo "Error: Virtual environment not found!"
    exit 1
fi

echo "Virtual environment activated successfully"
echo ""

# Run the test suite
echo "Running test suite with pytest..."
echo "================================"
python -m pytest test_app.py -v

# Capture the exit code
TEST_EXIT_CODE=$?

echo "================================"
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed successfully!"
    echo "Exit code: 0"
    exit 0
else
    echo "✗ Some tests failed!"
    echo "Exit code: 1"
    exit 1
fi
