#!/usr/bin/python3
import sys,os,re,time
import requests
import pexpect
import logging
from lqlpy import *


######################################################################
if __name__=='__main__':
    start = time.time()
    tshark_start()
    #set config
    supi='imsi-450051234000000'
    pdu_id = 7
    #get ip
    smfip = get_ip('root-test_smfsm_1')
    sctpmgr_ip = get_ip('root-test_sctpmgr_1')
    gnbip = get_ip('root-test_gnb_1')
    logging.info('*****sctpmgr ip is:'+sctpmgr_ip)
    logging.info('*******smfip ip is:'+smfip)
    logging.info('*******gnbip ip is:'+gnbip)
    #run init connection
    child_gnb = conn_gnb(sctpmgr_ip)
    child_upf = conn_upf()
######################################################################

    logging.info('step1-start gnb and ue')
    gnb_cli(child_gnb,cli='r a')
######################################################################
    logging.info('step2-start pdu session')
    num1=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_ESTB_REQ')
    num2=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_REQ')
    gnb_cli(child_gnb,cli='ule 0 0 7 1-abd001 inet1')
    logging.info(gnb_show(child_gnb,cli='show stat'))
    num3=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_ESTB_RSP')
    num4=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_MOD_RSP')
    bak = compare(num1,num3,1)
    bak1 = compare(num2,num4,1)
    if bak and bak1:
        logging.info('pdu session establishment successful')
    else:
        logging.error('pdu session establishment failure')
    get_pdu_session(smfip,supi,pdu_id)
    ue_ip = get_ue_ip()
    if ue_ip and child_upf:
        upf_display_ue(child_upf,ue_ip,rule='far')
        #upf_display_ue(child_upf,ue_ip,rule='qer')
        #upf_display_ue(child_upf,ue_ip,rule='pdr')
    else:
        logging.error('check 5gc procedure!')
######################################################################
    logging.info('step4-pdu session release procedure')
    num7=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_REQ')
    gnb_cli(child_gnb=child_gnb,cli='ulr 0 0 7 1-abd001 inet1')
    num8=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_RSP')
    bak3 = compare(num7,num8,1)
    if bak3:
        logging.info('pdu session release procedure successful!')
    else:
        logging.error('pdu session release procedure failure!')
######################################################################
    logging.info('step5-ue initiated deregistration procedure')
    num5=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_REQ')
    gnb_cli(child_gnb=child_gnb,cli='uld all')
    logging.info(gnb_show(child_gnb=child_gnb,cli='show stat'))
    num6=upf_check(child_upf,cmd='show upf stats pfcp msg | include SESS_DEL_RSP')
    bak2 = compare(num5,num6,0)
    if bak2:
        logging.info('ue initiated deregistration procedure successful!')
    else:
        logging.error('ue initiated deregistration procedure failure!')
######################################################################
    gnb_close(child_gnb)
    upf_close(child_upf)
    get_log()
    tshark_stop()
    tshark_show()
    tiplog()
    logging.info('spend time(s): '+str(time.time()-start))
