#!/bin/sh

if ! hash air &> /dev/null
then
    echo "AIR could not be found, running installation script"
    cd ../.. && make install-air && cd packages/api
fi

echo $PWD
air -c .air.toml