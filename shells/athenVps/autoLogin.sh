#!/bin/bash
PASSWORD="497197aa"
SERVER="root@27.126.181.90"

#so you firstly you need sshpass.
sshpass -p $PASSWORD ssh -o StrictHostKeyChecking=no $SERVER

# Pseudo-terminal will not be allocated because stdin is not a terminal

# ssh $SERVER <<EOF
# 	$PASSWORD
# EOF

