#!/usr/bin/python3
import paramiko
#import psutil
import os,time,re,sys
import logging
import requests
import configparser
#from datetime import datetime

#while true; do netstat -an | grep 8080; sleep 1; done

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

def route(container_ip,hostname):
    #route
    logging.info('Checking the route...')
    route = os.popen('route -n\n')
    context = route.read()
    #print(context)
    pattern = re.compile(container_ip,re.M)
    comparsion = pattern.search(context)
    if comparsion is None:
        logging.info('add route {}'.format(container_ip))
        routeadd = os.popen('route add -host {} gw {}\n'.format(container_ip,hostname))
    else:
        logging.warning('The route {} is exist!'.format(container_ip))
        pass

#get smfip
def get_ip_and_route(hostname,container,port=22):
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
        logging.debug(channel.recv(65535).decode(encoding='utf-8'))
        sys.stdout.flush()
        dockeripcmd = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'"
        channel.send('{} {}\n'.format(dockeripcmd,container))
        time.sleep(1)
        result_container = channel.recv(65535).decode(encoding='utf-8')
        #print(result_container)
        pattern_ip = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        container_ip = pattern_ip.search(result_container)
        if container_ip is None:
            logging.error(result_container)
        else:
            print('The container {} ip is:'.format(container))
            print(container_ip.group())
            logging.info('set docker route of {}'.format(container))
            sys.stdout.flush()
            channel.send('iptables -I DOCKER-USER --dst {}/32 -j ACCEPT\n'.format(container_ip.group()))
            time.sleep(1)
            logging.debug(channel.recv(65535).decode(encoding='utf-8'))

        channel.close()
        transport.close()
        return container_ip.group()

    except Exception as err:
            logging.error('peer options be failure!!! Reason is {}'.format(err))


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

    #get ip
    smf_ip = get_ip_and_route(hostname,container_smfsm)
    time.sleep(10)

    if smf_ip:
        #set route of peer
        route(smf_ip,hostname)
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
        #print(r.text)

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
        #print(r.text)

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
        #print(r.text)

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
        #print(r.text)

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
            #print(r.text)
            print(r.json())
            with open('text','w') as f:
                f.write(r.json())

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
        #print(r.text)

        #put log-interface/NSMF
        nif = ['db','nsmf','namf','npcf','nchf','nnrf','nssf','nudm','gtpc','pfcp','nas','ngap','etcd','mgmt','lql']
        for nl in nif:
            url = 'http://{}:80/mgmt/v1/log-interface/{}'.format(smf_ip,nl)
            headers = {"Accept": "application/json","Content-type": "application/json"}
            r = requests.put(url,headers=headers)
            logging.info('put '+r.url)
            print('The options respose code is:',r.status_code)
            if r.status_code != 200:
                logging.warning('response failure!')
            else:
                pass

    else:
        logging.error('Can not get smf ip!')

    end = time.time()
    logging.info('spend time(s): {}'.format(end-start))
