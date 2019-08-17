#!/usr/bin/python3

import os,sys,time,re

def tshark_start():
    os.system("nohup tshark -i any -f 'net 172.24.14.0/24' -w %s &" %(pcap_file))
    os.system('\n')

def tshark_stop():
    os.system('killall tshark')

pcap_file = 'tmp.pcap'

tshark_start()
print(1)
time.sleep(10)
print(2)
tshark_stop()
