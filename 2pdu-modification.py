#!/usr/bin/python3
import sys,os,re,time
import requests
import pexpect
import logging
from lqlpy import *


#############################################################################
if __name__=='__main__':
    start = time.time()
    #set config
    supi='imsi-450051234000000'
    pdu_id = 7
    #get ip
    smfip = get_ip('root-test_smfsm_1')
    sctpmgr_ip = get_ip('root-test_sctpmgr_1')
    logging.info('*****sctpmgr ip is:'+sctpmgr_ip)
    logging.info('*******smfip ip is:'+smfip)
    #run gnb start
    logging.info('step1-run pdu session')
    child_gnb=conn_gnb(sctpmgr_ip)
    gnb_cli(child_gnb=child_gnb,cli='r a')
    gnb_cli(child_gnb=child_gnb,cli='ule 0 0 7 1-abd001 inet1')
    
    logging.info('step2-check pdu session from upf')
    #gnb_show(child_gnb=child_gnb,cli='show stat')
    logging.info(gnb_show(child_gnb=child_gnb,cli='show stat'))
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
    #check pdu modification 
    check_mod=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_REQ')
    gnb_cli(child_gnb=child_gnb,cli='ulm 0 0 7 1-abd001 inet1')
    logging.info(gnb_show(child_gnb=child_gnb,cli='show stat'))
    check_mod1=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_RSP')
    if str.isnumeric(check_mod) and str.isnumeric(check_mod1):
        if int(check_mod1) == int(check_mod) +1:
            logging.info('ue initiated pdu session modification successful!')
        else:
            logging.error('ue initiated pdu session modification failure!')
    else:
        logging.error('check the show upf statis')

    #check pdu release
    check_del=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_REQ')
    gnb_cli(child_gnb=child_gnb,cli='uld all')
    logging.info(gnb_show(child_gnb=child_gnb,cli='show stat'))
    check_del1=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_RSP')
    if str.isnumeric(check_del) and str.isnumeric(check_del1):
        if int(check_del1) == int(check_del) +1:
            logging.info('ue initiated deregistration successful!')
            gnb_close(child_gnb)
            upf_close(child_upf)
        else:
            logging.error('ue initiated deregistration failure!')
            gnb_close(child_gnb)
            upf_close(child_upf)
    else:
        logging.error('check the show upf statis')
        gnb_close(child_gnb)
        upf_close(child_upf)
####################################################################################
    #spend time and running files
    logging.info('spend time(s): '+str(time.time()-start))
    tiplog()
