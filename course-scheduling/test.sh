#!/bin/bash

pip install -r ./requirements.txt


# Run the Python test script
echo "==============================="
python -m unittest tests/test.py
