#!/bin/bash

echo "Running parser debug test..."

# Project-Root
export PYTHONPATH=.

# runs the test with result in console
pytest -s tests/test_parser_output.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Parser test ran successfully!"
else
    echo "❌ Parser test failed!"
fi

exit $EXIT_CODE