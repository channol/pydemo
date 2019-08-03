#!/user/bin/python3
#https://github.com/secdev/scapy/blob/master/doc/notebooks/HTTP_2_Tuto.ipynb

import sys,os,time
from scapy.all import *
import scapy_http.http
import socket
import ssl

import scapy.supersocket as supersocket
import scapy.contrib.http2 as h2
import scapy.config

pkts = rdpcap("n1n2.pcap")
pkts1 = rdpcap("http1.pcap")

print(pkts)
print(pkts[0])
print(pkts[0].show())
print(pkts[0].sprintf('%Raw.load%'))

#print(pkts1)
#print(pkts1[0].show())

