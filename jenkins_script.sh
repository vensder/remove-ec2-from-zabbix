#!/usr/bin/env bash

set -e

python3 --version
virtualenv --version

PATH=$WORKSPACE/env3/bin:/usr/local/bin:$PATH
if [ ! -d "env3" ]; then
        virtualenv -p python3 env3
fi
. env3/bin/activate
pip install -r requirements.txt --download-cache=/tmp/$JOB_NAME
python --version
python remove_terminated_instances.py