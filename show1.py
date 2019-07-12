#!/usr/bin/env python3
import paramiko
import time
import os, sys
import re
#import netsnmp


##客户端信息
host='172.0.10.165'
port=22
username='casa'
password='casa'

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
