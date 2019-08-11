#!/usr/bin/python3
import os,sys,time

print('*******start capture and you can ctrl+c to stop wireshark!')
pcapf='test'+time.strftime('%Y_%m_%d_%H_%M_%S')+'.pcap'
logf='smfsm'+time.strftime('%Y_%m_%d_%H_%M_%S')+'.log'
os.system('tcpdump -i any net 172.24.14.0/24 -w /root/test/log/{}'.format(pcapf))
time.sleep(1)
print('******copy log file to /root/test/log/******')
os.system('cd /root/test/')
os.popen('dcomp logs smfsm > /root/test/log/{}'.format(logf))
time.sleep(3)
print('******bye!******')
print('\n')
print('log file name is:',logf)
print('scp root@172.0.5.27:/root/test/log/{} .'.format(logf))
print('vim scp://root@172.0.5.27//root/test/log/{}'.format(logf))
print('\n')
print('pcap file name is:',pcapf)
print('scp root@172.0.5.27:/root/test/log/{} .'.format(pcapf))
print('\n')
