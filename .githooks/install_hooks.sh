#!/bin/bash

current_directory=${PWD##*/} 
if [[ $current_directory != "spa-website-2022" ]]
then
    echo "Please run this script from the spa-website-2022 directory"
    exit 1
fi
ln -s $PWD/.githooks/pre-commit $PWD/.git/hooks/pre-commit 
chmod +x $PWD/.git/hooks/pre-commit
ls -l $PWD/.git/hooks/pre-commit
