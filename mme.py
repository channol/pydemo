#!/usr/bin/env python3

import netsnmp
import time

###def mme session
def MmeSession():
    MmeSession=netsnmp.Session(Version=2,
                               DestHost='172.0.14.250',
                               Community='public')
    return MmeSession
print(MmeSession())

mmebind1='CASA-GW-MIB::casaMmeTotalEnbSessions'
mmebind2='CASA-GW-MIB::casaMmeTotalUeSessions' 
mmebind3='CASA-GW-MIB::casaMmeTotalErabs'


