# Automatic host registration in zabbix using python and api-zabbix

[![Build Status](https://travis-ci.org/Emerson89/create-host.svg?branch=master)](https://travis-ci.org/Emerson89/create-host)

## Dependencies

- Python3.8
- zabbix_api

## Requirements
```
pip install -r requirements.txt
```
## Pattern:

# How to use

Lists the templates, groups and proxies, the proxy being optional if you don't use it, enter a value= 0

In the file hosts.csv insert the ips you want to register follow the example

## Set access to the zabbix-server front
```
python3 host_create.py http://x.x.x.x/zabbix Admin zabbix
```
## License
GPLv3