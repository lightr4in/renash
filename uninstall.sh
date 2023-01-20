#!/bin/bash

set -e

SCRIPT_PATH="renash/renash.py"
BIN_DIR="$HOME/.local/bin"
FILE_PATH="$BIN_DIR/$SCRIPT_PATH"

# Make sure the script file exists
if [ ! -f "$FILE_PATH" ]; then
  echo "Error: $FILE_PATH not found"
  exit 1
fi

# Remove the symbolic link in the bin directory
rm "$FILE_PATH"

echo "Uninstalled $SCRIPT_PATH from $BIN_DIR"
