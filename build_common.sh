#!/usr/bin/env bash

set -e # fail fast

here=`pwd`

cd common

# Clean any previously created files.
rm -rf dist

if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
    echo "Windows Environment"
    python setup.py sdist bdist_wheel
else
    echo "Not Windows Environment"
    python3 setup.py sdist bdist_wheel
fi

# Delete intermediate files.
rm -rf aist_common.egg-info
rm -rf build

pip install --ignore-installed dist/aist_common-0.0.1-py3-none-any.whl

cd $here