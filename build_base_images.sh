#!/usr/bin/env bash

set -e # fail fast

here=`pwd`

# We push the image below to DockerHub as it takes a while to build.
# Keep this commented out unless there is a need to push a new image to DockerHub.
# docker build -f deployment/aist-python-base/Dockerfile -t aista-python-base .

docker build -f deployment/aist-python/Dockerfile -t aist-python .

docker build -f deployment/aist-tensorflow/Dockerfile -t aist-tensorflow .

cd $here
