#!/usr/bin/python3
import paramiko
#import psutil
import os,time,re,sys
import logging
import requests
import configparser
from datetime import datetime

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

def route():
    #route
    logging.info('Checking the route 172.24.14.0/24...')
    route = os.popen('route -n\n')
    context = route.read()
    #print(context)
    pattern = re.compile(r'172.24.14.0',re.M)
    comparsion = pattern.search(context)
    if comparsion is None:
        logging.info('add route to 172.24.14.0/24')
        routeadd = os.popen('route add -net 172.24.14.0/24 gw 172.0.5.27\n')
    else:
        logging.info('The route is exist!')
        pass

#get smfip
def get_ip(hostname,container,port=22):
    try:
        logging.info('connecting host {} ...'.format(hostname))
        transport = paramiko.Transport(hostname,port)
        transport.connect(username='root',password='casa')
        logging.info('Connecting host {} is successful!'.format(hostname))
        channel = transport.open_session()
        channel.settimeout(3)
        channel.get_pty()
        channel.invoke_shell()
        channel.send('date\n')
        time.sleep(1)
        channel.send('iptables -I DOCKER-USER --dst 172.24.14.0/24 -j ACCEPT\n')
        time.sleep(1)
        connectioninfo = channel.recv(65535).decode(encoding='utf-8')
        #logging.info(connectioninfo)
        sys.stdout.flush()
        dockeripcmd = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'"
        channel.send('{} {}\n'.format(dockeripcmd,container))
        time.sleep(1)
        result_container = channel.recv(65535).decode(encoding='utf-8')
        #print(result_container)
        pattern_ip = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        container_ip = pattern_ip.search(result_container)
        print('The container ip is:')
        print(container_ip.group())
        #print(container_ip)
        channel.close()
        transport.close()
        return container_ip.group()

    except Exception as err:
            logging.info('Connecting host {} is failure!!! Reason is {}'.format(hostname,err))


if __name__=='__main__':
    start = time.time()
    #config
    config = configparser.ConfigParser()
    config.read('./config/smf.config')

    hostname = config.get('smf','hostname')
    supi = config.get('smf','supi')
    pdu_id = config.get('smf','pdu_id')
    container_smfsm = config.get('smf','container_smfsm')
    container_udm = config.get('smf','container_udm')
    pdu_id = config.get('smf','pdu_id')

    #set route
    route()

    #get ip
    smf_ip = get_ip(hostname,container_smfsm)
    time.sleep(1)
    #udm_ip = get_ip(hostname,container_udm)
    #time.sleep(1)

    if smf_ip:
        #put 
        url = 'http://{}:80/mgmt/v1/log-filter/{}'.format(smf_ip,supi)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        #print(url)
        r = requests.put(url,headers=headers)
        #print(r.url)
        logging.info('put '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)

        #delete
        url = 'http://{}:80/mgmt/v1/log-filter/{}'.format(smf_ip,supi)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.delete(url,headers=headers)
        logging.info('delete '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)

        #put log-interface/NSMF
        url = 'http://{}:80/mgmt/v1/log-interface/nsmf'.format(smf_ip)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.put(url,headers=headers)
        logging.info('put '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)

        #delete log-interface/NSMF
        url = 'http://{}:80/mgmt/v1/log-interface/nsmf'.format(smf_ip)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.delete(url,headers=headers)
        logging.info('delete '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)

        #get sesssion pdu id
        url = 'http://{}:80/mgmt/v1/session/{}/{}'.format(smf_ip,supi,pdu_id)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.get(url,headers=headers)
        logging.info('get '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)

        #delete sesssion pdu id
        url = 'http://{}:80/mgmt/v1/session/{}/{}'.format(smf_ip,supi,pdu_id)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.delete(url,headers=headers)
        logging.info('delete '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        print(r.text)
    else:
        logging.info('Can not get smf ip!')

    end = time.time()
    print(datetime.now())
    logging.info('spend time: {}'.format(end-start))
