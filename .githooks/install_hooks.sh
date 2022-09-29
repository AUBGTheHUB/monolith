#!/bin/bash

# In case we decide not to use the Make phony
current_directory=${PWD##*/} 
if [[ $current_directory != "spa-website-2022" ]]
then
    echo "Please run this script from the spa-website-2022 directory"
    exit 1
fi

# symlink pre-commit
ln -s $PWD/.githooks/pre-commit $PWD/.git/hooks/pre-commit 
chmod +x $PWD/.git/hooks/pre-commit
ls -l $PWD/.git/hooks/pre-commit

# symlink post-commit
ln -s $PWD/.githooks/post-commit $PWD/.git/hooks/post-commit
chmod +x $PWD/.git/hooks/post-commit
ls -l $PWD/.git/hooks/post-commit

