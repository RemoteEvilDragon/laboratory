#!/bin/bash
subdir="subdirectory"
test -d $subdir || mkdir $subdir

cd $subdir

rm -rf *
list="dir1 dir2 dir3"
for dir in $list 
do
   mkdir $dir
done

for dir in $list 
do
   cd $dir
   touch "$dir.info"
   cd ..
done
