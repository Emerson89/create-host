from zabbix_api import ZabbixAPI
import csv

URL = 'http://x.x.x.x/zabbix'
USERNAME = 'Admin'
PASSWORD = 'senhazabbix'

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "2": {"type": "SNMP", "id": "2", "port": "161"},
}

groupids = ['15']
groups = [{"groupid": groupid} for groupid in groupids]
            
'''
interface = {
    "type": info_interfaces['1']['id'],
    "main": 1,
    "useip": 1,
    "ip": "192.168.33.50",
    "dns": "",
    "port": info_interfaces['1']['port']
}
'''

def create_host(host, ip):
    try:
        create_host = zapi.host.create({
            "groups": groups,
            "host": host,
            "templates": [{"templateid":"10001"}],
            "interfaces": {
                "type": info_interfaces['1']['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces['1']['port']
}
        })
        print(f'Host cadastrado {host}')
    except Exception as err:
        print(f'Falha ao cadastrar {err}')
    
with open('hosts.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [ipaddress] in file_csv:
        create_host(host=ipaddress,ip=ipaddress)