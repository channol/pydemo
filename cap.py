#!/usr/bin/python3
import os,sys,time

#tshark_path = '/opt/wireshark/wireshark-3.0.3-built/tshark'
#capture = pyshark.LiveCapture(output_file="./debug/test.pcap",interface="any",tshark_path=tshark_path)
#capture.sniff(timeout=120)
print('*******start capture and you can ctrl+c to stop wireshark!')
os.system('tcpdump -i any net 172.24.14.0/24 -w ./debug/test{}.pcap'.format(time.strftime('%Y_%m_%d_%H_%M_%S')))
#os.system('tcpdump -i any -w ./debug/test{}.pcap'.format(time.strftime('%Y_%m_%d_%H_%M_%S')))
time.sleep(1)
print('******copy log file to /root/test/debug/******')
os.popen('dcomp logs smfsm > ./debug/test{}.log'.format(time.strftime('%Y_%m_%d_%H_%M_%S')))
time.sleep(3)
print('******check the debug files******')
print(os.popen('ls -lh /root/test/debug').read())
time.sleep(1)
print('******bye!******')
time.sleep(1)
