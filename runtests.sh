#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [ -z "$VIRTUAL_ENV" ]; then
	echo "Please activate your environment first!"
	exit 1;
fi

if [ "$1" = "--jenkins" ]; then
	nosetests --with-xunit;
	./pep8.sh
else
	while [ 1 ]; do 
		nosetests --processes=2 $*;
		./pep8.sh;
		sleep 2;
		clear;
	done
fi
