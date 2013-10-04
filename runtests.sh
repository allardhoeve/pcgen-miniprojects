#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

if [ -z "$VIRTUAL_ENV" ]; then
	if [ -e "../bin/activate" ]; then
		echo "Activating your environment for you"
		. ../bin/activate
	else 
		echo "Please activate your environment first!"
	fi
fi

if [ "$1" = "--jenkins" ]; then
	nosetests --with-xunit;
	./pep8.sh
else
	watch -c -- "
		nosetests --color $*;
		./pep8.sh"
fi
