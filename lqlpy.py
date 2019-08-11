#!/usr/bin/python3
import sys,os,re,time
import requests
import pexpect
import logging

#set result file and log file
st = time.strftime('%Y_%m_%d_%H_%M_%S')
#result_file = '/root/test/log/result'+time.strftime('%Y_%m_%d_%H_%M_%S')+'.log'
result_file = '/root/test/log/result'+st+'.log'
log_file = '/root/test/log/running'+st+'.log'

#set logging config
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#set file handler of logging
file_handler = logging.FileHandler(log_file,mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d %H:%M:%S %a'))
logger.addHandler(file_handler)
#set console handler of logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s",datefmt='%Y-%m-%d %H:%M:%S %a'))
logger.addHandler(console_handler)

##########################################################
def get_ip(container):
    #get container ip 
    result = os.popen("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %s" %(container))
    ip = result.read().replace('\n',"")
    return ip 

def get_pdu_session(smfip,supi,pdu_id):
    #get supi session information
    if len(smfip) == 0:
        logging.error('SMF ip is NULL! Please check!')
    else:
        url = 'http://{}:80/mgmt/v1/session/{}/{}'.format(smfip,supi,pdu_id)
        headers = {"Accept": "application/json","Content-type": "application/json"}
        r = requests.get(url,headers=headers)
        logging.info('Get '+r.url)
        rsp_code = r.status_code
        logging.info('The options respose code is:'+str(r.status_code))
        if r.status_code != 200:
            logging.error('Get pdu session failure!')
        else:
            logging.info(r.json())
            with open(result_file,'w') as f:
                f.write(r.json())

def get_ue_ip():
    #get ue ip for smf
    if os.path.exists(result_file):
        ue_ip=os.popen("awk '/ipaddr/' %s | awk -F \"\\\"\" '{print $4}'" %(result_file)).read().replace('\n',"")
        return ue_ip
    else:
        pass

def conn_upf():
    #connect upf
    upf_login = "ssh test@172.0.5.38"
    child_upf = pexpect.spawn(upf_login)
    index_upf = child_upf.expect(['password: ',pexpect.EOF,pexpect.TIMEOUT])
    if index_upf != 0:
        logging.error('connect to upf failure!')
        child_upf.close()
    else:
        child_upf.sendline('testcasa')
        time.sleep(1)
        child_upf.expect('CASA-MOBILE>')
        time.sleep(1)
        child_upf.sendline('page-off')
        time.sleep(1)
        child_upf.expect('CASA-MOBILE>')
        time.sleep(1)
        return child_upf

def upf_close(child_upf):
    if child_upf:
        child_upf.close()
        
def upf_display_ue(child_upf,ue_ip,rule):
    #send cli to upf
    child_upf.buffer
    time.sleep(1)
    child_upf.sendline("show upf session ue-ip {} {}".format(ue_ip,rule))
    time.sleep(1)
    index_ue = child_upf.expect(['session not found','CASA-MOBILE>'])
    time.sleep(1)
    if index_ue == 0:
        logging.error('UPF can not find the session')
    else:
        logging.info(child_upf.before.decode(encoding='utf-8'))
        if os.path.exists(result_file):       
            with open(result_file,'a') as f:
                f.write(child_upf.before.decode(encoding='utf-8'))
        else:
            logging.error('Can not wirte to result file!')

def upf_check(child_upf,cmd):
    child_upf.buffer
    time.sleep(1)
    child_upf.sendline(cmd)
    time.sleep(1)
    index_check = child_upf.expect(['Syntax Error','CASA-MOBILE>'])
    if index_check == 0:
        logging.error('UPF can check error!')
    else:
        check = child_upf.before.decode(encoding='utf-8')
        check_num = re.search('\d+',check,re.M)
        if check_num is None:
            logging.error('result is None!')
            if os.path.exists(result_file):       
                with open(result_file,'a') as f:
                    f.write(cmd)
                    f.write(check_num)
            else:
                logging.error('Can not wirte to result file!')
        else:
            logging.info(cmd)
            logging.info('check result: '+check_num.group())
            if os.path.exists(result_file):       
                with open(result_file,'a') as f:
                    f.write(cmd)
                    f.write('\n')
                    f.write('result: ')
                    f.write(check_num.group())
                    f.write('\n')
            else:
                logging.error('Can not wirte to result file!')
            #retun result number
            return check_num.group()

def conn_gnb(sctpmgr_ip):
    #connect to sim-gnb
    gnblogin = 'docker exec -it root-test_gnb_1 sh'
    child_gnb = pexpect.spawn(gnblogin)
    index_gnb = child_gnb.expect(['/ #',pexpect.EOF,pexpect.TIMEOUT])
    if index_gnb != 0:
        logging.error('enter sim-gnb failure!')
        child_gnb.close()
    else:
        child_gnb.sendline('killall sim-gnb')
        time.sleep(1)
        child_gnb.expect('/ #')
        child_gnb.sendline('\nsim-gnb -h 38412 -p 38412 -d  10.27.0.1 -n 1 -u 1 -B 65501 -a {}'.format(sctpmgr_ip))
        index_init = child_gnb.expect([' diag> create cpe raw socket success on interface:eth0',pexpect.EOF,pexpect.TIMEOUT])
        if index_init != 0:
            logging.error('start sim-gnb cmd failure!')
            child_gnb.close()
        else:
            logging.info('start sim-gnb cmd successful!')
            child_gnb.sendline('\nset imsi mcc 450 mnv 05 msin 1234000000')
            time.sleep(1)
            index_imsi = child_gnb.expect(['[Ii]nvalid',' diag>'])
            if index_imsi == 0:
                logging.error('set imsi-450051234000000 failure!')
                logging.info('enter diag cli and check!')
                child_gnb.interact()
            else:
                logging.info('set imsi-450051234000000 successful!')
                return child_gnb

def gnb_cli(child_gnb,cli):
    #sim-gnb send cli
    if child_gnb:
        child_gnb.sendline('\n')
        child_gnb.expect(' diag>')
        time.sleep(1)
        child_gnb.buffer
        child_gnb.sendline(cli)
        time.sleep(3)
        index_cli = child_gnb.expect([' diag> .',pexpect.EOF,pexpect.TIMEOUT])
        if index_cli != 0:
            logging.info('send cli failure! Check the cli : {}'.format(cli))
            child_gnb.interact()
        else:
            logging.info('send cli successful! The cli: {}'.format(cli))
            time.sleep(3)

    else:
        logging.error('check the connection of sim-gnb')

def gnb_show(child_gnb,cli):
    #sim-gnb show cli
    if child_gnb:
        child_gnb.expect(' diag> ')
        time.sleep(1)
        child_gnb.buffer
        child_gnb.sendline(cli)
        time.sleep(1)
        child_gnb.expect(' diag> ')
        time.sleep(1)
        show = child_gnb.before
        show_rsp = show.decode(encoding='utf-8')
        #logging.info(show_rsp)
        return show_rsp

    else:
        logging.error('check the connection of sim-gnb')

def gnb_close(child_gnb):
    #child_gnb = conn_gnb(sctpmgr_ip)
    if child_gnb:
        child_gnb.close()

def tiplog():
    if os.path.exists(result_file):
        logging.info('The information file: '+result_file)
    else:
        logging.warning('The information file is not exist!')
    if os.path.exists(log_file):
        logging.info('The running log file: '+log_file)
    else:
        logging.warning('The running log file is not exist!')

