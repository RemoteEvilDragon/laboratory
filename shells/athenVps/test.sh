#!/bin/bash

# test=$1

# echo ${test##*/}

# list=$(ls)

# echo $list

# if [[ -d $1 ]] ; then
#   echo "$1 is a directory"
# fi

# function iterDir(){
# 	for f in $(ls $1) ; do
# 		sub="$1/$f"
# 		if [[ -d $sub ]] ; then
# 			echo "$f is a directory"
# 			iterDir "$1/$f"
# 		elif [[ -f $sub ]] ; then
# 			echo "$f is an file"
# 		fi
# 	done
# }
# iterDir $1

declare -a list
declare -i count=0

echo $count

# filelist=$(ls $1)
# for f in $filelist ; do
# 	echo $f
# 	w="$"
# 	if [[ -d $f ]] ; then
# 		echo "$f is a directory"
# 	elif [[ -f $f ]] ; then
# 		echo "$f is an file"
# 	fi
# done
