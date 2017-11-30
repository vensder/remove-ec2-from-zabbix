# Remove terminated AWS EC2 instances from Zabbix

Python 3 supported.

This script check availability of AWS EC2 instances in Zabbix, and if they not exists in the default AWS region (because of termination for ex.), they will be removed from Zabbix.

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

docker logs -f ec2-cleaner