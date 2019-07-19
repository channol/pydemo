#!/usr/bin/python3
import paramiko
#import psutil
import os,time,re,sys
import logging
import requests

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d  %H:%M:%S %a')

#route
route = os.popen('route -n\n')
context = route.read()
#print(context)
pattern = re.compile(r'172.24.14.0',re.M)
comparsion = pattern.search(context)
if comparsion is None:
    logging.info('add route to 172.24.14.0/24')
    routeadd = os.popen('route add -net 172.24.14.0/24 gw 172.0.5.27\n')
else:
    pass

#get smfip
def smfip(hostname,port=22):
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
        connectioninfo = channel.recv(65535).decode(encoding='utf-8')
        sys.stdout.flush()
        dockeripcmd = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' root-test_smfsm_1\n"
        channel.send(dockeripcmd)
        time.sleep(1)
        result_container = channel.recv(65535).decode(encoding='utf-8')
        #print(result_container)
        pattern_ip = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        container_ip = pattern_ip.search(result_container)
        print('The container smfsm ip:',container_ip.group())
        #print(container_ip)
        channel.close()
        transport.close()
        return container_ip.group()

    except Exception as err:
            logging.info('Connecting host {} is failure!!! Reason is {}'.format(hostname,err))



#config
setion = 'log-filter/'
supi = '12345678901234'
setion1 = 'log-interface/'
interface = 'NSMF'
setion2 = 'session/'
pduid = '/5'
hostname = '172.0.5.27'
port = 22


#smfip = '172.24.14.5'
smfip = smfip(hostname)

#put
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion+supi
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.put(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)

#delete
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion+supi
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.delete(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)

#put log-interface/NSMF
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion1+interface
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.put(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)

#delete log-interface/NSMF
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion1+interface
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.delete(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)

#get log-interface/NSMF
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion2+supi+pduid
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.get(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)

#delete log-interface/NSMF
url = 'http://{}:80/mgmt/v1/'.format(smfip)+setion2+supi+pduid
headers = {"Accept": "application/json","Content-type": "application/json"}
r = requests.delete(url,headers=headers)
logging.info(url)
print('respose code is:',r.status_code)
print(r.text)
