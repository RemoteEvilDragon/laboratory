#!/bin/bash
clear

echo "Start script"
echo "Hi,$USER!"
echo

echo "a list of connected users:"
echo
set -x
w
set +x
echo

echo "Setting two variables now."
COLOUR="black"
VALUE="9"

echo "a string:$COLOUR"
echo "a number:$VALUE"
echo
