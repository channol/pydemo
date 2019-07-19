#!/usr/bin/python3
import paramiko
import psutil
import os,time,re,sys
import logging

def process(process,hostname):
    try:
        logging.info('connecting host {} ...'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('Connecting host {} is successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        time.sleep(1)
        channel.send('')

    except Exception as err:
        logging.error('Try to connect host {} failure!'.format(hostname))

#logging.basicConfig(logging.level=logging.INFO)
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')


