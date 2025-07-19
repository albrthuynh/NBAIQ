#!/bin/bash

# Script to run API tests for the NBA IQ App

echo "Setting up test environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install test dependencies
echo "Installing test dependencies..."
pip install -r requirements-test.txt

# Run tests
echo "Running API tests..."
python -m pytest test_api.py -v --tb=short

echo "Test run complete!"
