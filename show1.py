#!/usr/bin/env python3
import paramiko
import time
import os, sys
import re
import netsnmp
import json





##客户端信息
host='172.0.10.165'
port=22
username='casa'
password='casa'

##初始化net-snmp
mmebind = {
1: 'CASA-NFV-MME-MIB::casaMmeTotalEnbSessions',
2: 'CASA-NFV-MME-MIB::casaMmeTotalUeSessions',
3: 'CASA-NFV-MME-MIB::casaMmeTotalErabs',
4: 'CASA-NFV-MME-MIB::casaMmeEnbInfoTable',
5: 'CASA-NFV-MME-MIB::casaMmeEnbInfoEntry', 
6: 'CASA-NFV-MME-MIB::casaMmeEnbId', 
7: 'CASA-NFV-MME-MIB::casaMmeEnbGlobalEnbId', 
8: 'CASA-NFV-MME-MIB::casaMmeEnbSctpIpAddress',
9: 'CASA-NFV-MME-MIB::casaMmeEnbSctpPort', 
10: 'CASA-NFV-MME-MIB::casaMmeUeInfoTable', 
11: 'CASA-NFV-MME-MIB::casaMmeUeInfoEntry', 
12: 'CASA-NFV-MME-MIB::casaMmeUeTmsi', 
13: 'CASA-NFV-MME-MIB::casaMmeUeImsi', 
14: 'CASA-NFV-MME-MIB::casaMmeUeGlobalEnbId', 
15: 'CASA-NFV-MME-MIB::casaMmeUeStatus',
16: 'CASA-NFV-MME-MIB::casaMmeSgwNodeTable',
17: 'CASA-NFV-MME-MIB::casaMmeSgwNodeEntry', 
18: 'CASA-NFV-MME-MIB::casaMmeSgwIpAddress', 
19: 'CASA-NFV-MME-MIB::casaMmeSgwIpPort'
}

##def showcli
def showcli(cmd):
    "showcli"
    transport=paramiko.Transport(host,port)
    transport.connect(username=username,password=password)
    channel=transport.open_session()
    channel.settimeout(3)
    channel.get_pty()
    channel.invoke_shell()
    channel.send(cmd)
    time.sleep(1)
    show_context=channel.recv(65535)
    transport.close()
    return show_context

##def snmpop
def snmpget(oid):
    "snmp operations"
    snmpsess=netsnmp.Session(Version=2,DestHost=host,Community='public')
    vars=netsnmp.VarList(netsnmp.Varbind(oid,0))
    snmp_context=snmpsess.get(vars)
    return snmp_context


if __name__ == '__main__':
    #get snmp
    snmp_context=snmpget(mmebind[1])
    snmp_result=snmp_context[0].decode(encoding='utf-8')
    print(snmp_result)

    #get cli 
    show_context = showcli('show mme info\r')
    print("="*20,"CLI display","="*20)
    clidisplay=show_context.decode(encoding='utf-8')
    print(clidisplay)
    #print(show_context)
    #data=json.dumps(clidisplay)
    #print(data)
    ##get cli statis
    resub=re.compile(r's1ap\sconnections\s+\d+\s+',re.M)
    result=resub.search(clidisplay)
    print(re.m



