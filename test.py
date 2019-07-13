#!/usr/bin/env/python3
import paramiko
import os,sys,re,time
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a')
                    #filename='./log/check.log',
                    #filemode='w')

host_mme = '172.0.5.35'
host_gw = '172.0.5.36'
host_sgw = '172.0.5.37'
host_pgw = '172.0.5.38'
port=22
username='root'
password='casa'
cmd='show mme info\r'
cmd1='show task crash\r'
cmd2='show version\r'

def transport(hostname,port=22):
    try:
        logging.info('init connecting to host {}'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username=username,password=password)
        logging.info('Connect to host {} successful!'.format(hostname))
        return transport
    except Exception as e:
        logging.error('Try to connect host {} failure! The reason is {}'.format(hostname,e))


def cli(transport,command):
    channel = transport.open_session()
    logging.info(channel.get_transport())
    channel.settimeout(3)
    channel.get_pty()
    channel.invoke_shell()
    channel.send('/usr/local/bin/casa/casa-cli\n')
    time.sleep(1)
    logging.debug(channel.recv(65535).decode(encoding='utf-8'))
    sys.stdout.flush()  #clear init connection info
    channel.send(command)
    time.sleep(3)
    cli_bytes=channel.recv(65535)
    cli=cli_bytes.decode(encoding='utf-8')
    logging.info(cli)
    channel.close()
    logging.info(channel.get_transport())
    transport.close()
    channel.get_transport()
    logging.info(channel.get_transport())

#    logging.info('END!')

if __name__ == '__main__':
    transport = transport(host_mme)
    cli(transport,cmd1)
    #cli(transport,cmd1)
    #cli(transport,cmd2)
    transport1 = transport(host_mme)
    cli(transport1,cmd1)
