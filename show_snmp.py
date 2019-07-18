#!/usr/bin/env python3
# snmp
#snmp test files
# import netsnmp
#pip install python3-netsnmp
## netsnmp github
#https://pypi.org/project/python3-netsnmp/

import paramiko
import time
import os, sys
import re


##客户端信息
host='172.0.10.165'
port=22
username='casa'
password='casa'

##初始化net-snmp

mmebind = {
'casaMmeTotalEnbSessions': '1.3.6.1.4.1.20858.10.104.9.1.1',
'casaMmeTotalUeSessions': '1.3.6.1.4.1.20858.10.104.9.1.2',
'casaMmeTotalErabs': '1.3.6.1.4.1.20858.10.104.9.1.3'
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

if __name__ == '__main__':
    start=time.time()

    show_context = showcli('show mme enodebs list\r')
    print("="*20,"CLI display","="*20)
    clidisplay=show_context.decode(encoding='utf-8')
    print(clidisplay)
    resub=re.compile(r'total\sENBs\s+\d+\s+',re.M)
    result=resub.search(clidisplay)
    if result:
        print("======match=====")
        #print(result.group())
        mun=re.search(r'\d+',result.group())
        print('TotalEnbSessions:',mun.group())
    else:
        print('match failed!!!')

    snmpcmd='snmpget -m all -v 2c -c public 172.0.10.165 1.3.6.1.4.1.20858.10.104.9.1.2.0'
    snmpresult=os.popen(snmpcmd).readline()
    print(snmpresult)

    #snmpnum=re.search(r'=\sCounter32:\s\d+\s+',snmpresult,re.M|re.S)
    snmpnum=re.search(r'\d+$',snmpresult,re.M|re.S)
    print(snmpnum.group())

    if snmpnum.group()==mun.group():
        print('pass!!')
    else:
        print('failed!!')
        print(snmpnum.group(),"vs",mun.group())

    end=time.time()
    spend_time = end - start
    print("Spend time:",spend_time)
