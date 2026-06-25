#!/bin/bash

echo "Running tests..."

pytest -v

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed!"
fi

exit $EXIT_CODE