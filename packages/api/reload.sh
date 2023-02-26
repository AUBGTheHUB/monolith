#!/bin/sh

if ! hash air &> /dev/null
then
    echo "AIR could not be found, running installation script"
    cd ../.. && make install-air
fi

air -c .air.toml