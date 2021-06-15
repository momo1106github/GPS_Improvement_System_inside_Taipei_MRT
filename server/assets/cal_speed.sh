#!/bin/zsh

filename=$1
echo ${filename}

# n=0
# while read line
# do
#	if [[ $(($n%2)) -eq 1 ]]; then
#		echo $line
#
#	fi
#	(( n++ ))
#done < $filename

awk '{ print (FNR % 2 == 0) ? ($1" "$2" "$1/$2"m/s") : $0 }' $filename > "new_${filename}"
