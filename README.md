# Automatic host registration in zabbix using python and api-zabbix

## Dependencies

- Python3.8
- zabbix_api
- zabbix 4.4

# How to use

In the file hosts.csv insert the ips you want to register

## Set access to the zabbix-server front
```
URL = 'http://x.x.x.x/zabbix'
USERNAME = 'Admin'
PASSWORD = 'senhazabbix'

python3 host_create.py
```
## License
GLPv3