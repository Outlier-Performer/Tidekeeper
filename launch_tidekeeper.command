#!/bin/bash
set -eu

cd "$(dirname "$0")"

if [ -x ".venv/bin/python" ]; then
    python=".venv/bin/python"
else
    python="$(command -v python3 || true)"
fi

if [ -z "$python" ]; then
    echo "Python 3 was not found. Install Python 3.10 or newer and try again."
    read -r -p "Press Return to close..."
    exit 1
fi

if ! "$python" -c "import pygame" >/dev/null 2>&1; then
    echo "Pygame is not installed for this Python environment."
    echo "In Terminal, run: python3 -m pip install -r requirements.txt"
    read -r -p "Press Return to close..."
    exit 1
fi

exec "$python" main.py
