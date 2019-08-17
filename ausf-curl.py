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
    container_ausf = config.get('smf','container_ausf')
    pdu_id = config.get('smf','pdu_id')

    #get ip
    #smf_ip = get_ip_and_route(hostname,container_smfsm)
    ausf_ip = get_ip_and_route(hostname,container_ausf)
    time.sleep(10)

    #headers = {"Accept": "application/json","Content-type": "application/json"}
    headers = {"authority": "sim-ausf",
                "method": "POST",
                "path": "/nausf-auth/v1/ue-authentications",
                "scheme": "http",
                "content-type": "application/json",
                "accept": "application/json",
                "user-agent": "OpenAPI-Generator/1.0.0/go",
                "content-length": "105",
                "accept-encoding": "gzip"}

    headers1 = {"authority": "sim-ausf",
                "method": "PUT",
                "path": "/nausf-auth/v1/ue-authentications/suci-0-450-05-?0-0-0-1234000000/5g-aka-confirmation",
                "scheme": "http",
                "content-type": "application/json",
                "accept": "application/json",
                "user-agent": "OpenAPI-Generator/1.0.0/go",
                "content-length": "47",
                "accept-encoding": "gzip"}

    payload_post = {"supiOrSuci":"suci-0-450-05-?0-0-0-1234000000","servingNetworkName":"5G:mnc005.mcc450.3gppnetwork.org"}
    payload_put = {"resStar":"9573b8155fde12d9d1258bb085d564d2"}

    if ausf_ip:
        #set route of peer
        route(ausf_ip,hostname)
        #put 
        url = 'http://{}:80/nausf-auth/v1/ue-authentications'.format(ausf_ip)
        #headers = {"Accept": "application/json","Content-type": "application/json"}
        #print(url)
        r = requests.post(url,headers=headers,json=payload_post)
        #print(r.url)
        logging.info('post '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 201:
            logging.warning('response failure!')
        else:
            pass
        #print(r.text)

        url = 'http://{}:80/nausf-auth/v1/ue-authentications/suci-0-450-05-?0-0-0-1234000000/5g-aka-confirmation'.format(ausf_ip)
        #headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.put(url,headers=headers1,json=payload_put)
        logging.info('put '+r.url)
        print('The options respose code is:',r.status_code)
        if r.status_code != 200:
            logging.warning('response failure!')
        else:
            pass
        #print(r.text)

    else:
        logging.error('Can not get container ip!')

    end = time.time()
    logging.info('spend time(s): {}'.format(end-start))
