#!/bin/bash

set -e

SCRIPT_PATH="renash/renash.py"
BIN_DIR="$HOME/.local/bin"

# Make sure the script file exists
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: $SCRIPT_PATH not found"
  exit 1
fi

# Create the bin directory if it does not exist
if [ ! -d "$BIN_DIR" ]; then
  mkdir -p "$BIN_DIR"
fi

# Create a symbolic link to the script in the bin directory
ln -s "$(pwd)/$SCRIPT_PATH" "$BIN_DIR/$SCRIPT_PATH"

echo "Installed $SCRIPT_PATH to $BIN_DIR"
