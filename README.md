# Automatic host registration in zabbix using python and api-zabbix

## Dependencies

- Python3.8
- zabbix_api
- zabbix 4.4

## Pattern:

- linux template;
- groupid Discovered hosts;
- Change the ids in the scripts;
- If you use uncommon proxy in the script and enter the id

# How to use

In the file hosts.csv insert the ips you want to register

## Set access to the zabbix-server front
```
python3 host_create.py http://x.x.x.x/zabbix Admin zabbix
```
## License
GPLv3