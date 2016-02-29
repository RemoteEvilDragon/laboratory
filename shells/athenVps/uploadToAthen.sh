#!/bin/bash
USERNAME="athenking"
PASSWORD="freedom"
SERVER="27.126.181.90"

# CLIENTDIR=$1
SERVERDIR=""

if [[ -d $1 ]]; then
  SERVERDIR=${1##*/}
fi

declare -a list
declare -i count=0

function copy_file (){
	for f in $(ls $1) ; do
		sub="$1/$f"
		if [[ -d $sub ]]; then
			subDir=${f##*/}
			list[$count]="mkdir $f"
			count=$count+1

			list[$count]="cd $f"
			count=$count+1
			SERVERDIR="$SERVERDIR/$f"

			copy_file $sub
		elif [[ -f $sub ]]; then
			list[$count]="put $sub $SERVERDIR/$f"
			count=$count+1
		fi
	done
}

copy_file $1

# echo "${list[*]}"
ftp -n -i $SERVER <<EOF
	user $USERNAME $PASSWORD
	binary
	${list[*]}
	exit
EOF

