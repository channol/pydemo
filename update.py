#!/usr/bin/python3

import paramiko
import os,sys,re,time
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt="%Y-%m-%d %H:%M:%S %a")

def update(version,hostname,port=22):
    try:
        logging.info('start copy version from 172.0.5.90:/pubilc/nfv-build/')
        logging.info('login server {}'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('login server {} successful'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        channel.send('/usr/local/bin/casa/casa-cli\n')
        time.sleep(1)
        logging.debug(channel.recv(65535).decode(encoding='utf-8'))
        sys.stdout.flush()
        channel.send('enable\r')
        while True:
            rst = str(channel.recv(1024))
            logging.info(rst)
            if 'Password:' in rst:
                channel.send('casa\r')
                time.sleep(3)
                break
        channel.send('copy scp root 172.0.5.90 /version/nfv-builds/5.0.0-111/casa-nfv-5.0.0-111.tar.gz nvram

