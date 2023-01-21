#!/bin/bash

set -e

SCRIPT_NAME="renash"
SCRIPT_PATH="renash/$SCRIPT_NAME"
BIN_DIR="$HOME/.local/bin"

SCRIPT_SRC_PATH="$(pwd)/$SCRIPT_PATH.py"

# Make sure the script file exists
if [ ! -f "$SCRIPT_SRC_PATH" ]; then
  echo "Error: $SCRIPT_SRC_PATH not found"
  exit 1
fi

# Create the bin directory if it does not exist
if [ ! -d "$BIN_DIR" ]; then
  mkdir -p "$BIN_DIR"
fi

# Create a symbolic link to the script in the bin directory
ln -s "$SCRIPT_SRC_PATH" "$BIN_DIR/$SCRIPT_NAME"

echo "Installed $SCRIPT_SRC_PATH to $BIN_DIR"
