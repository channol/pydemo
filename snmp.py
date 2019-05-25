#!/usr/bin/env python3
import netsnmp
import time
import paramiko

saegwip='172.0.20.16'
mmeip='172.0.10.165'

testip=mmeip

testuser='casa'
password='casa'

sess=netsnmp.Session(Version=2,
                    DestHost=testip,
                    Community='public')

#sess.UseSprintValue=1
##
mmebind = {
1: 'CASA-NFV-MME-MIB::casaMmeTotalEnbSessions',
2: 'CASA-NFV-MME-MIB::casaMmeTotalUeSessions',
3: 'CASA-NFV-MME-MIB::casaMmeTotalErabs',
4: 'CASA-NFV-MME-MIB::casaMmeEnbInfoTable',
5: 'CASA-NFV-MME-MIB::casaMmeEnbInfoEntry', 
6: 'CASA-NFV-MME-MIB::casaMmeEnbId', 
7: 'CASA-NFV-MME-MIB::casaMmeEnbGlobalEnbId', 
8: 'CASA-NFV-MME-MIB::casaMmeEnbSctpIpAddress',
9: 'CASA-NFV-MME-MIB::casaMmeEnbSctpPort', 
10: 'CASA-NFV-MME-MIB::casaMmeUeInfoTable', 
11: 'CASA-NFV-MME-MIB::casaMmeUeInfoEntry', 
12: 'CASA-NFV-MME-MIB::casaMmeUeTmsi', 
13: 'CASA-NFV-MME-MIB::casaMmeUeImsi', 
14: 'CASA-NFV-MME-MIB::casaMmeUeGlobalEnbId', 
15: 'CASA-NFV-MME-MIB::casaMmeUeStatus',
16: 'CASA-NFV-MME-MIB::casaMmeSgwNodeTable',
17: 'CASA-NFV-MME-MIB::casaMmeSgwNodeEntry', 
18: 'CASA-NFV-MME-MIB::casaMmeSgwIpAddress', 
19: 'CASA-NFV-MME-MIB::casaMmeSgwIpPort'
}

##循环
#for i in range(1,3):
#   vars = netsnmp.VarList(netsnmp.Varbind(mmebind[i],0))                   
#    vals=sess.get(vars)
#    print(i,mmebind[i],"=",vals)
vars = netsnmp.VarList(netsnmp.Varbind(mmebind[1],0))
vals=sess.get(vars)
print('======1.mib enb sessions======')
print(1,mmebind[1],"=",vals)
##paramiko
print('======2.check cli======')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=testip,port=22,username='root',password="casa")
stdin,stdout,stderr = ssh.exec_command("ls")
#stdin,stdout,stderr = ssh.exec_command("/usr/local/bin/casa/casa-cli")
#stdin,stdout,stderr = ssh.exec_command("show mme enodebs list \| include \"total ENBs\"")
print('===cmd putout====')
for line in stdout:
    print(line.strip('\n'))
#result = stdout.read()
#print(result)
