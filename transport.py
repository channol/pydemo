#!/usr/bin/python3
import netsnmp
import time
import paramiko


saegwip='172.0.20.16'
mmeip='172.0.10.165'

testip=mmeip

testuser='casa'
passwd='casa'

t=paramiko.Transport(mmeip,22)
t.connect(username=testuser,password=passwd)
chan=t.open_session()
chan.settimeout(3)
chan.get_pty()
chan.invoke_shell()
print("============")
chan.send("show mme info\r")
time.sleep(1)
str=chan.recv(65535)
print(str.decode(encoding='utf-8'))
t.close()

