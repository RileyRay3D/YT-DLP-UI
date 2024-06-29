#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH="python"
SCRIPT_PATH="$SCRIPT_DIR/yt_dlp_ui.py"

# Run the Python script
nohup "$PYTHON_PATH" "$SCRIPT_PATH" > /dev/null 2>&1 &
