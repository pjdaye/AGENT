#!/usr/bin/env bash

set -e # fail fast

here=`pwd`

pip install -r $(sed -e 's/ / -r /g' <<< $(ls components/*/requirements.txt))

cd $here
