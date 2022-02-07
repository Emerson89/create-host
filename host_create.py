#!/usr/bin/python3

from zabbix_api import ZabbixAPI,Already_Exists
import csv
import sys
import getpass
import time
import getpass

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Digite a senha: ")

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

#Funçao procura templates
def procurando_templates(nome_template):
    id = zapi.template.get({
        "output": ['name', 'templateid'],
        "search": {"name": '*' + nome_template + '*'},
        "searchWildcardsEnabled": True
    })
    if id:
        print("***Template encontrados***")
        print()
        #Condicao se e for para procura templateid e nome
        for x in id:
            print ("TemplateID: {} {} Nome: {}\n".format(x['templateid'],'-', x['name']))
    else:
        print("***Template não encontrado***")
#Input de entrada para pesquisa nome template
nome_template = input("Pesquise nome de um template não precisa ser completo: ")
print()
procurando_templates(nome_template)
print()
#Variavel armazena o id do template
TEMPLATE = input("Insira o templateid...: ")
print ()
def procurando_groupid(nome_group):
    hostgroups = zapi.hostgroup.get({
            "output": ['name','groupid'], 
            "sortfield": "name",
            "search": {"name": '*' + nome_group + '*'},
            "searchWildcardsEnabled": True
    })
    if hostgroups:
        print("***Groups encontrados***")
        print()
        for x in hostgroups:
            print ("GroupID: {} {} Nome: {}\n".format(x['groupid'],'-', x['name']))
    else:
        print("***Group não encontrado***")
nome_group = input("Pesquise nome de um group não precisa ser completo: ")
print()
procurando_groupid(nome_group)
print()
GROUP = input("Insira o groupid...: ")
print()
print('***Listando proxys***')
print()
idproxy = zapi.proxy.get({
    "output": "extend", 
    "sortfield": "host"
    })
for x in idproxy:
    print ("ProxyID: {} {} Nome: {}\n".format(x['proxyid'],'-', x['host']))
print()
PROXY = input("Digite o proxyid caso não utilize insira 0: ")
print()
print("***Tipos de interfaces possíveis: 1 - agent; 2 - SNMP***")
print()
TYPEID = input("Insira o typeid...: ")
print()
DESCRIPTION = input("Deseja inserir alguma descrição? Caso Não deixe em branco: ")
print()
print('Aguarde...')
time.sleep(2)
print()

info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "2": {"type": "SNMP", "id": "2", "port": "161"},
}

groupids = [GROUP]
groups = [{"groupid": groupid} for groupid in groupids]
            
def create_host(nomes, host, ip):
    try:
        create_host = zapi.host.create({
            "groups": groups,
            "host": host,
            "name": nomes,
            "description": DESCRIPTION,
            "templates": [{"templateid":TEMPLATE}],
            "proxy_hostid": PROXY,
            "interfaces": {
                "type": info_interfaces[TYPEID]['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces[TYPEID]['port'],
                "details": {
                    "version": 2,
                    "bulk": 1,
                    "community": "{$SNMP_COMMUNITY}"
                }
            }
        })
        print(f'Host cadastrado {host}')
    except Already_Exists:
        print(f'Host(s) já cadastrado {host}')
    except Exception as err:
        print(f'Falha ao cadastrar {err}')
   
with open('hosts.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [nome,hosts,ipaddress] in file_csv:
        create_host(nomes=nome,host=hosts,ip=ipaddress)

zapi.logout()