#!/bin/bash
clear
echo "This is information provided by mysystem.sh.Program starts now."

echo "Hello,$USER"
echo

echo "Today's date is"
date
echo

echo "These users are currently connected:"
w|cut -d " " l - | grep -v USER | sort -u
echo

echo "This is 'unmae -s' running on a 'uname -m' processor."
echo

echo "This is the uptime information:"
uptime
echo

echo "That's all forks!"
