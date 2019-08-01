#!/usr/bin/python3
#import pyshark
import os,sys,time
import pexpect

#tshark_path = '/opt/wireshark/wireshark-3.0.3-built/tshark'
#capture = pyshark.LiveCapture(output_file="./debug/test.pcap",interface="any",tshark_path=tshark_path)
#capture.sniff(TIMEOUT=120)

prompt = 'diag> '
cmd = 'dcomp exec gnb sh'

#index 
print('start sim-gnb docker')
child = pexpect.spawn(cmd)
index = child.expect(['/ #',pexpect.EOF,pexpect.TIMEOUT])
if index != 0:
    print('enter docker failure')
    child.close()
else:
    print('enter docker gnb successful!')

    #start sim gnb and kill old process
    print('run---sim-gnb -h 38412 -p 38412 -d  10.27.0.1 -n 1 -u 1 -B 65501 -a 172.24.14.9')
    child.sendline('killall sim-gnb')
    time.sleep(1)
    child.sendline('\nsim-gnb -h 38412 -p 38412 -d  10.27.0.1 -n 1 -u 1 -B 65501 -a 172.24.14.9')
    time.sleep(1)
    index1 = child.expect([' diag> create cpe raw socket success on interface:eth0',pexpect.EOF,pexpect.TIMEOUT])
    if index1 != 0:
        print('start sim-gnb cmd failure>>>')
        child.close()
    else:
        print('start sim-gnb cmd successful!')

        #set imsi
        print('set imsi 450051234000000')
        child.sendline('\nset imsi mcc 450 mnv 05 msin 1234000000')
        time.sleep(1)
        #index = child.expect(['[Ii]nvalid',pexpect.EOF,pexpect.TIMEOUT])
        index = child.expect(['[Ii]nvalid',' diag>'])
        if index == 0:
            print('set imsi failure')
            print('enter diag and check the setting')
            child.interact()
        else:
            print('set imst successful')
            time.sleep(1)

            #send ngap setup request cmd
            print('send ngap setup request and ue register')
            child.sendline('r a')
            time.sleep(5)
            index = child.expect(['diag> .',pexpect.EOF,pexpect.TIMEOUT])
            if index != 0:
                print('send ngap request failure and check the setting!')
                child.interact()
            else:
                print('send ngap request successful!')
                print('wait for time 5s.............')
                time.sleep(5)

                #send supi session pdu establishment request cmd
                print('send session pdu establishment request cmd:ule 0 0 7 1 inet1')
                child.sendline('ule 0 0 7 1 inet1')
                time.sleep(5)
                index = child.expect(['diag> .',pexpect.EOF,pexpect.TIMEOUT])
                if index != 0:
                    print('send pdu establishment request failure and check the setting!')
                    child.interact()
                else:
                    print('send pdu establishment request successful!')
                    print('wait for time 5s.............')
                    time.sleep(5)

                    child.sendline('show ms')
                    child.expect('diag> ')
                    child.sendline('show stat')
                    child.expect('diag> ')
                    result=child.before
                    cli= result.decode(encoding='utf-8')
                    print(cli)


                    i = input("enter 'y' to cli or others to contniue update and release session: ")
                    if i=='y':
                        child.interact()
                    else:
                        #send pdu session update
                        print('send pdu session update!')
                        child.sendline('ulm 0 0 7 1 inet1')
                        time.sleep(5)
                        index = child.expect(['diag> .',pexpect.EOF,pexpect.TIMEOUT])
                        if index !=0:
                            print('send pdu session update failure!')
                            child.interact()
                        else:
                            print('send pdu session update successful!')
                            print('wait for time 5s.............')
                            time.sleep(5)

                            #send session release
                            print('pdu session release!')
                            child.sendline('uld all')
                            time.sleep(5)
                            index = child.expect(['diag> .',pexpect.EOF,pexpect.TIMEOUT])
                            if index !=0:
                                print('send pdu session release fauilure and check the setting!')
                                child.interact()
                            else:
                                print('send pdu session release successful!')
                                print('wait for time 5s.............')

                                #child.interact()
                                s = input("enter 'y' to cli or others exit:  ")
                                if s=='y':
                                    child.interact()
                                else:
                                    child.close()

