#!/bin/bash

echo 'test test test'

# final exe

fzf_path="/usr/share/fzf"

if [[ -x "$(command -v fzf)" && -d $fzf_path ]]; then
    if [[ -f "${fzf_path}/key-bindings.bash" && -f "${fzf_path}/completion.bash" ]]; then
        source "${fzf_path}/key-bindings.bash"
        source "${fzf_path}/completion.bash"
    fi
fi

# just test
if [[ "" != "$(command -v fzf)" ]]; then
    echo "fzf command exits"
    echo command -v fzf
fi

if [[ -x "$(command -v fzf)" && -d $fzf_path ]]; then
    echo "fzf is an executable"
    echo "$(command -v fzf)"
else
    echo "fzf is not an executable"
fi

if [[ -d "$fzf_path" ]]; then
    echo "$fzf_path exits"
    if [[ -f "${fzf_path}/key-bindings.bash" && -f "${fzf_path}/completion.bash" ]]; then
        echo "key-bindings.bash exist"
        source "${fzf_path}/key-bindings.bash"
        source "${fzf_path}/completion.bash"
        echo "sourcing files"
    fi
fi
