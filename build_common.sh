#!/usr/bin/env bash

here=`pwd`

cd common
python3 setup.py sdist bdist_wheel

# Delete intermediate files.
rm -rf aist_common.egg-info
rm -rf build

pip install --ignore-installed dist/aist_common-0.0.1-py3-none-any.whl

cd $here