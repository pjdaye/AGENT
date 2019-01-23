#!/usr/bin/env bash

here=`pwd`

docker build -f deployment/aist-python/Dockerfile -t aist-python .

docker build -f deployment/aist-tensorflow/Dockerfile -t aist-tensorflow .

cd $here
