#!/usr/bin/python3
import sys,os,re,time
import requests
import pexpect
import logging
from lqlpy import *


#############################################################################
if __name__=='__main__':
    #set config
    supi='imsi-450051234000000'
    pdu_id = 7
    smfip = get_ip('root-test_smfsm_1')
    sctpmgr_ip = get_ip('root-test_sctpmgr_1')
    logging.info('*****sctpmgr ip is:'+sctpmgr_ip)
    logging.info('*******smfip ip is:'+smfip)

    logging.info('step1-run pdu session')
    child_gnb=conn_gnb(sctpmgr_ip)
    gnb_cli(child_gnb=child_gnb,cli='r a')
    gnb_cli(child_gnb=child_gnb,cli='ule 0 0 7 1-abd001 inet1')
    
    logging.info('step2-check pdu session from upf')
    gnb_show(child_gnb=child_gnb,cli='show stat')
    get_pdu_session(smfip,supi,pdu_id)
    ue_ip = get_ue_ip()
    child_upf = conn_upf()
    logging.info('*********ue ip is:'+str(ue_ip))
    if ue_ip and child_upf:
        upf_display_ue(child_upf=child_upf,ue_ip=ue_ip,rule='far')
        upf_display_ue(child_upf=child_upf,ue_ip=ue_ip,rule='qer')
        upf_display_ue(child_upf=child_upf,ue_ip=ue_ip,rule='pdr')
    else:
        logging.error('check upf spawn!')

##################################################################################
    i=input('choice：\n\
            y--enter diag cli\n\
            m--modification pdu\n\
            r--release pdu\n\
            other--ue deregistration\n\
            enter: ')
    logging.info(i)
    i=='xterm-256colory' or i=='y' or i == 'PuTTYy'
    if i=='xterm-256colory' or i=='y' or i == 'PuTTYy':
        child_gnb.interact()
    elif i=='xterm-256colorm' or i=='m' or i == 'PuTTYm':
        check_num=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_REQ')
        gnb_cli(child_gnb=child_gnb,cli='ulm 0 0 7 1-abd001 inet1')
        check_num1=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_RSP')
        if str.isnumeric(check_num) and str.isnumeric(check_num1):
            if int(check_num1) == int(check_num) +1:
                logging.info('pdu modification successful!')
            else:
                logging.error('pdu modification failure!')
        else:
            logging.error('check the show upf statis')
        gnb_cli(child_gnb=child_gnb,cli='uld all')
        gnb_close(child_gnb)
        upf_close(child_upf)

    elif i=='xterm-256colorr' or i=='r' or i == 'PuTTYr':
        gnb_cli(child_gnb=child_gnb,cli='\nulr all')
        gnb_close(child_gnb)
        upf_close(child_upf)

    else:
        gnb_cli(child_gnb=child_gnb,cli='\nuld all')
        gnb_close(child_gnb)
        upf_close(child_upf)

    if os.path.exists(result_file):
        logging.info('The ue information file: '+result_file)
    if os.path.exists(log_file):
        logging.info('The running log file: '+log_file)
