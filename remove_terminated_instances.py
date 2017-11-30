#!/usr/bin/env python3

from zabbix_api import ZabbixAPI
from boto import ec2
import os

if all(var in os.environ for var in ["ZABBIX_USER", "ZABBIX_PASSWORD", "ZABBIX_URL"]):
    zapi = ZabbixAPI(server=os.environ.get('ZABBIX_URL')) 
    zapi.validate_certs = False 
    zapi.login(os.environ.get('ZABBIX_USER'), os.environ.get('ZABBIX_PASSWORD'))
    zapi.timeout = 30
else:
    raise Exception("Zabbix environment variables are not defined")

zabbix_unavailable_hosts_IPs = set()
ec2_active_instances_IPs = set()

# Get hosts with unavailable zabbix-agents (list from dicts): [{dict},]
zabbix_unavailable_hosts_ids = zapi.host.get({"output": ["hostid"], "filter": {"available": ["2"]}}) 
# [{'hostid': '10280'}, ...]

# Get hosts IP-id (list from dicts): [{dict},]
zabbix_hosts_ids_IPs = zapi.hostinterface.get({"output": ["ip", "hostid"]})
# [{'hostid': '10084', 'interfaceid': '1', 'ip': '172.31.10.205'}, ...]

for hostid in zabbix_unavailable_hosts_ids:
    for item in zabbix_hosts_ids_IPs:
        if hostid.get('hostid') == item.get('hostid'):
            zabbix_unavailable_hosts_IPs.add(item.get('ip'))

if all(var in os.environ for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]):
    ec2conn = ec2.connect_to_region(os.environ.get('AWS_DEFAULT_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
else:
    raise Exception("AWS access credentials environment variables are not set")

reservations = ec2conn.get_all_instances()
instances = [i for r in reservations for i in r.instances]
for i in instances:
    ec2_active_instances_IPs.add(i.private_ip_address)

# This Zabbix hosts absent in EC2:
ec2_terminated_istances_IPs = zabbix_unavailable_hosts_IPs - ec2_active_instances_IPs

zabbix_hosts_ids_to_delete = []

for hostid in zabbix_hosts_ids_IPs:
    for ip in ec2_terminated_istances_IPs:
        if hostid.get('ip') == ip:
            zabbix_hosts_ids_to_delete.append(hostid.get('hostid'))

if zabbix_hosts_ids_to_delete:
    print("These hosts will be deleted from Zabbix: {0}".format(zabbix_hosts_ids_to_delete))
    zapi.host.delete(zabbix_hosts_ids_to_delete)
else:
    print("Nothing to remove")
