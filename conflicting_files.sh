#!/bin/bash

:'\nwhen Package Manager (pacman or paru) is unable to update new packages
an Error comes up in the Terminal with message
"error: failed to commit transaction (conflicting files)"
with an append of all the file paths of those confliciting files
this is meant for an automatic resolution of the problem\n'

# take realpath of current file ($0)
# then get the directory path and save in dir_path
dir_path=$(dirname $(realpath $0))
file_name="conflicting_files.txt"
output_file="$dir_path/$file_name"

echo -e '\n calling pacman for new packages \n'
OUTPUT="$(sudo pacman -Syu)"
echo -e $OUTPUT > $output_file
echo "$(cat $output_file | grep -o '\/\S*')" > $output_file

while read line; do
    resolve="$(pacman -Qo $line)"
    echo $resolve
    if [[ $resovle==*"No package owns"* ]]; then
    # TODO: better rename file to file.bak and then try command again and then if all goes well delete
        sudo rm $line
        echo "package removed!"
    else
        echo "$resolve from package $line"
    fi
done < $output_file

echo "conflict resolved!"

rm $output_file
