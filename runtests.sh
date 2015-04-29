#!/bin/bash
set -e
set -u

numprocs=-1
RUN_ONCE=""
jenkins=""

#FLAKE8_CMD="flake8 --ignore=E501 ."
FLAKE8_CMD="pep8 --ignore=E501 ."

export LC_NUMERIC="en_US.UTF-8"
export PYTHONPATH=.

while getopts "1js" opt; do
  case $opt in
    1) RUN_ONCE=1;;
    j) jenkins=1;;
    s) numprocs=0;;
  esac
done

shift $((OPTIND-1))

if [ $(uname) = "Darwin" ]; then
    MACOSX=1
else
    MACOSX=0
    if [ "$jenkins" != 1 ]; then    
        if test ! -x "/usr/bin/inotifywait"; then
            echo "Cannot find inotifywait, please run:"
            echo "apt-get install inotify-tools"
            exit 1;
        fi
    fi
fi    



run_full_tests () {
    set +e
    nosetests --processes=$numprocs --process-timeout=20 $*
    $FLAKE8_CMD
}




if [ "$jenkins" = 1 ]; then
    export PYTHONDONTWRITEBYTECODE=1  # Avoid .pyc files that can mess up coverage
	python manage.py test  
        $FLAKE8_CMD
else
    if [ -z $RUN_ONCE ]; then

	clear
	run_full_tests $*

        while true; do
	    if [ "$MACOSX" = "1" ]; then
		sleep 5
	    	clear;
		run_full_tests $*
	    else
            	echo
	    	echo "Will rerun tests when changes are detected in your repository"
            	echo
	    	inotifywait -qre modify .
            	echo "Rerunning, please wait..."
            	echo
            	clear;
	    	run_full_tests $*
    	    fi
        done
    else
	run_full_tests $*
    fi
fi
