#!/usr/bin/env sh

if [ -z "$1" ]; then
  echo "Enter the name of the script you wish to execute as an argument."
  exit 1
fi

SCRIPT_NAME="$1"

python "./src/${SCRIPT_NAME}" "$@"
