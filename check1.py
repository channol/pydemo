#!/usr/bin/env/python3
import paramiko
import os,sys,re,time
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a')
                    #filename='./log/check.log',
                    #filemode='w')

hostname='172.0.5.35'
port=22
username='test'
password='casa1234'
cmd='show mme info\r'
cmd1='show task crash\r'
try:
    logging.info('init connecting to host {}'.format(hostname))
    transport = paramiko.Transport(hostname,port)
    transport.connect(username=username,password=password)
    channel = transport.open_session()
    channel.settimeout(3)
    channel.get_pty()
    channel.invoke_shell()
    channel.send(cmd)
    time.sleep(3)
    channel.send(cmd1)
    time.sleep(3)
    showmmeinfo_bytes=channel.recv(65535)
    showmmeinfo=showmmeinfo_bytes.decode(encoding='utf-8')
#    print(showmmeinfo_bytes)
    logging.info(showmmeinfo)
    transport.close()
    logging.info('END!')
except Exception as e:
    logging.error('The host {} connecting failure! The reason is {}'.format(hostname,e))

