# Remove terminated AWS EC2 instances from Zabbix

Python 3 supported.

This script check availability of AWS EC2 instances in Zabbix, and if they not exist in the default AWS region (because of termination for ex.), they will be removed from Zabbix.

Script runs periodically with $TIMEOUT, which you can set as environment variable.

## Environment variables

Set this environment variables inside the docker container or on the host, if you would like to run it directly. Zabbix API user should have read/write permissions.

```yaml
     - ZABBIX_USER=<zabbix_api_user>
     - ZABBIX_PASSWORD=<zabbix_api_password>
     - ZABBIX_URL=https://<url_or_ip>
     - AWS_ACCESS_KEY_ID=<access_id>
     - AWS_SECRET_ACCESS_KEY=<access_key>
     - AWS_DEFAULT_REGION=us-west-2
     - TIMEOUT=30
     - PYTHONUNBUFFERED=1
```

## Run it in docker with docker-compose

```sh
docker-compose up -d
```

## Watch logs

```sh
docker logs -f ec2-cleaner
```

## Run it in Jenkins


Add String and Password Parameters into the Job (environment variables).

Add Git Source Code Management:

Repository URL: https://github.com/vensder/remove-ec2-from-zabbix.git

Add build step "Execute shell" in Jenkins job:

```sh
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
```

Python 3 and vitrualenv should be installed on the host.