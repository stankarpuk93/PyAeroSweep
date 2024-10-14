#!/bin/bash

# echo $1
# echo $2
# echo $3
 echo $4
Ask_Password="Password for: "$1
echo $Ask_Password
read -s  password

# make temp folder
tempfolder=$2/tempfolder
make_tempfolder="mkdir $tempfolder && exit"
remove_tempfolder="rm -r $tempfolder && exit"

sshpass -p $password ssh $1 $remove_tempfolder
sshpass -p $password ssh $1 $make_tempfolder

# Copy to temp folder
remote_dir="$1:$2/tempfolder"
sshpass -p $password scp -r $3 $remote_dir

# Copy from temp to cases
copy_command="cp -rT --backup=existing --backup=numbered --reflink=auto  $2/tempfolder/ $2 && exit"
sshpass -p $password ssh $1 $copy_command


# remove temp folder--backup=numbered
sshpass -p $password ssh $1 $remove_tempfolder


echo "Copy_to_remote.sh: finished"




