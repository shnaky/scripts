#!/bin/bash

file="mull.txt"
filtered_file="mull_filtered.txt"

# command paru and write output to file while also have interactive stdout
paru |& tee $file

# filter the output file with regex and add it in new file
echo "$(cat $file | rg -o \/home[@/\\w.-]* )" > $filtered_file

# read filtered file and remove all files in verbose mode
while read line; do
    echo $line
    resolve=$(sudo rm -rv $line)
    echo $resolve
done < $filtered_file

rm -v mull.txt
rm -v mull_filtered.txt
echo "files removed"
