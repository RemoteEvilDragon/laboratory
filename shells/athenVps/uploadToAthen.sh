#!/bin/sh

USERNAME="athenking"
PASSWORD="freedom"
SERVER="27.126.181.90"
DIR=$1
FILE=$2

cd $DIR
ftp -n -i $SERVER <<EOF
user $USERNAME $PASSWORD
binary
put "$DIR/$FILE" $FILE
exit
EOF