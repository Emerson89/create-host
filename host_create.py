from zabbix_api import ZabbixAPI
import csv
import sys

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

print('Listando Templateids')
print ()
id = zapi.template.get({"output": "extend"})
for x in id:
    print (x['templateid'], "-", x['name'])
print()
TEMPLATE = input("Insira o templateid...: ")
print ()
print('Listando groupsids...')
print()
hostgroups = zapi.hostgroup.get({"output": "extend", "sortfield": "name"})
for x in hostgroups:
    print (x['groupid'], "-", x['name'])
print()
GROUP = input("Insira o groupid...: ")
print()
print('Listando proxyids...')
idproxy = zapi.proxy.get({"output": "extend", "selectInterface": "extend"})
for x in idproxy:
    print (x['proxyid'], "-", x['description'])
print()
PROXY = input("Insira o proxyid...: ")
print()
print("Types de interfaces possíveis valores são: 1 - agent; 2 - SNMP ")
print()
TYPEID = input("Insira o typeid...: ")

info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "2": {"type": "SNMP", "id": "2", "port": "161"},
}

groupids = [GROUP]
groups = [{"groupid": groupid} for groupid in groupids]
            
def create_host(host, ip):
    try:
        create_host = zapi.host.create({
            "groups": groups,
            "host": host,
            "templates": [{"templateid":TEMPLATE}],
            "proxy_hostid": PROXY,
            "interfaces": {
                "type": info_interfaces[TYPEID]['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces[TYPEID]['port']
}
        })
        print()
        print(f'Host cadastrado {host}')
    except Exception as err:
        print(f'Falha ao cadastrar {err}')
    
with open('hosts.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [nome,ipaddress] in file_csv:
        create_host(host=nome,ip=ipaddress)