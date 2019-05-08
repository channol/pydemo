#!/usr/bin/python3
import netsnmp
import time

sess=netsnmp.Session(Version=2,
                    DestHost='172.0.20.16',
                    Community='public')


print(1)
#sess.UseSprintValue=1

print(2)
#henbgw=netsnmp.Varbind('sysUptime',0)
vars = netsnmp.VarList(netsnmp.Varbind('sysUpTime', 0),
                       netsnmp.Varbind('CASA-NFV-HA-MIB::casaHaHeartBeatMsgRecv', 0),
                       netsnmp.Varbind('CASA-NFV-HA-MIB::casaHaHeartBeatMsgSent', 0))
                       
vals=sess.get(vars)

print(vals)
