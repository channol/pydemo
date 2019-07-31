#!/usr/bin/python3

import paramiko
import os,time,re,sys
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

def dockerip(hostname,port=22):
    try:
        logging.info('connecting host {} ...'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('Connecting host {} is successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        channel.send("\ndocker inspect --format='{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)\n")
        time.sleep(1)
        result1 = channel.recv(65535).decode(encoding='utf-8')
        print(result1)
        channel.close()
        transport.close()

    except Exception as err:
        logging.error('Connecting host {} is failure!!! Reason is {}'.format(hostname,err))
        transport.close()


if __name__ == '__main__':
    hostname='172.0.5.27'
    port=22
    dockerip(hostname,port)


