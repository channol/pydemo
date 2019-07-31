#!/usr/bin/python3
import pexpect

host = '172.0.5.25'
path = '/tmp/epc-check.log'
password = 'casa'

cmd = "scp root@"+host+":"+path+" ."

child = pexpect.spawn(cmd)
index = child.expect(["root@172.0.5.25's password: ",pexpect.EOF,pexpect.TIMEOUT])
if index !=0:
    print('login failure')
else:
    child.sendline(password)
    print('login and copy')
    child.expect(pexpect.EOF)
    child.close()

