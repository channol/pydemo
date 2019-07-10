#!/usr/bin/env/python3
import paramiko
import os,sys,re,time
import logging


#logging.basicConfig(level=logging.INFO)

class RemoteModel:
    """remote options model and execute remote command"""

    def __init__(self,hostname,port=22,username='casa',password='casa'):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.session = None
        self.init_conn()

    def init_conn(self):
        """init connection host"""
        try:
            logging.info('setp_1:init connecting to host {}'.format(self.hostname))
            self.transport = paramiko.Transport(self.hostname,self.port)
            self.session = self.transport.connect(username=self.username,password=self.password)
        except Exception as e:
            logging.error('The host {} connecting failure! The reason is {}'.format(self.hostname,e))

    def close(self):
        """close connection"""
        if self.session:
            self.session.close()
            self = None

    def execute_command(self,command):
        """ execute command and return the response lines"""
        channel = self.transport.open_session()
        #channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        channel.send(command)
        channel.recv(65535)
        response=channel.recv(65535)
        response_decode=response.decode(encoding='utf-8')
        print(1)
        print(response_decode)
        #logging.info(response_decode)
#        channel.close()
        return response_decode


if __name__=='__main__':
    hostname='172.0.10.165'
    port=22
    username='casa'
    password='casa'
    command='show mme info\r'
    swp=RemoteModel(hostname,port,username,password)
    swp.execute_command(command)
