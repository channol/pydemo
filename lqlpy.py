#!/usr/bin/python3
import sys,os,re,time
import requests
import pexpect
import logging

#set result file and log file
strftime = time.strftime('%Y_%m_%d_%H_%M_%S')
report = 'report'+strftime
os.makedirs('/root/test/log/{}'.format(report))
def file_name(filename):
    file_name = '/root/test/log/{}/{}'.format(report,filename)+strftime+'.log'
    return file_name
result_file = file_name('result')
running_file = file_name('running')
smfsm_file = file_name('smfsm')
pcap_file = '/root/test/log/'+report+'/pcap'+strftime+'.pcap'

with open(result_file,'w') as f:
    f.write(strftime)

#####################################################
#set logging config
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#set file handler of logging
file_handler = logging.FileHandler(running_file,mode='w')
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
            #logging.info(r.json())
            with open(result_file,'a') as f:
                f.write(r.json())

def get_ue_ip():
    #get ue ip for smf
    if os.path.exists(result_file):
        ue_ip=os.popen("awk '/ipaddr/' %s | awk -F \"\\\"\" '{print $4}'" %(result_file)).read().replace('\n',"")
        ue_state=os.popen("awk '/fsmState/' %s" %(result_file)).read().replace('\n',"")
        logging.info('The ue ip is:'+str(ue_ip))
        logging.info('The ue state is:'+str(ue_state))
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

def compare(num1,num2,thereshold):
    if str.isnumeric(num1) and str.isnumeric(num2):
        n = int(num2) - int(num1)
        if n == int(thereshold):
            logging.info('The compare step running successful!')
            return True
        else:
            logging.error('The compare step running failure!')
            return False
    else:
        logging.error('Please check statis numbers!')
        return False

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
            return True
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
        child_gnb.sendcontrol('c')
        child_gnb.expect('/ #')
        child_gnb.close()

def get_log(node='smfsm'):
    os.chdir('/root/test/')
    os.popen('dcomp logs {} > {}'.format(node,smfsm_file))

def tshark_start():
    #os.system("nohup tshark -i any -f 'net 172.24.14.0/24' -w %s &" %(pcap_file))
    os.system("nohup tcpdump -i any -f 'net 172.24.14.0/24' -w %s &" %(pcap_file))
    logging.info('start tshark')

def tshark_stop():
    os.system('killall tcpdump')
    logging.info('stop tshark')

def tshark_show():
    logging.info('show pcap file with http2 and pfcp')
    show = os.popen("tshark -r %s -Y 'pfcp or http2'" %(pcap_file))
    with open ('tmp.log','w') as f:
        f.write(show.read())
    logging.info('show file is tmp.log')

def tiplog():
    if os.path.exists(result_file):
        logging.info('The information file: '+result_file)
    else:
        logging.warning('The information file is not exist!')

    if os.path.exists(running_file):
        logging.info('The running log file: '+running_file)
    else:
        logging.warning('The running log file is not exist!')

    if os.path.exists(smfsm_file):
        logging.info('The smfsm log file: '+smfsm_file)
        logging.info('scp root@172.0.5.27:'+smfsm_file+' .')
        logging.info('vim scp://root@172.0.5.27/'+smfsm_file)
    else:
        logging.warning('The smfsm log file is not exist!')

    if os.path.exists(pcap_file):
        logging.info('The pcap file: '+pcap_file)
        logging.info('scp root@172.0.5.27:'+pcap_file+' .')
    else:
        logging.warning('The pcap file is not exist!')

