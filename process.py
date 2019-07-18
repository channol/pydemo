#!/usr/bin/python3

import psutil
import os,time,re,sys

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
