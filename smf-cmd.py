#!/usr/bin/python3
import paramiko
import psutil
import os,time,re,sys
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

#def transport(hostname,port=22):
#    try:
#        logging.info('connecting host {} ...'.format(hostname))
#        transport = paramiko.Transport(hostname,port)
#        transport.connect(username='root',password='casa')
#        logging.info('Connecting host {} is successful!'.format(hostname))
#        return transport
#    except Exception as err:
#        logging.error('Try to connect failure! Error: {}'.format(err))
#
#def check(transport,command):
#    try:
#        channel = transport.open_session()
#        channel.settimeout(3)
#        channel.get_pty()
#        channel.invoke_shell()
#        time.sleep(1)
#        channel.send('ls\n')
#        time.sleep(1)
#        logging.info(channel.recv(65535).decode(encoding='utf-8'))
#        time.sleep(3)
#        channel.close()
#    except Exception as e:
#        logging.error('channel failure! {}'.format(e))

smfcmd = "curl --http2-prior-knowledge -H "Accept: application/json" -H "Content-type: application/json" -X " + 
curl --http2-prior-knowledge -H "Accept: application/json" -H "Content-type: application/json" -X PUT   http://172.24.14.7:80/mgmt/v1/log-filter/12345678901234

if __name__ =='__main__':
    transport = transport('172.0.10.165')
    check(transport)
    time.sleep(3)
    transport.close()


