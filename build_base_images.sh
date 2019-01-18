#!/usr/bin/env bash

here=`pwd`

docker build -f deployment/aist-python/Dockerfile -t aist-python .

cd $here
