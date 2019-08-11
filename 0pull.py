#!/usr/bin/python3

import sys,os,re,time
from datetime import datetime

images = {
    'PFCP_IMG':'registry.gitlab.casa-systems.com/mobility/smf/pfcp',
    'UDM_IMG':'registry.gitlab.casa-systems.com/mobility/sim-udm',
    'SMFSM_IMG':'registry.gitlab.casa-systems.com/mobility/smf/sm',
    'UEMGR_IMG':'registry.gitlab.casa-systems.com/mobility/amf/uemgr',
    'N2MGR_IMG':'registry.gitlab.casa-systems.com/mobility/amf/n2mgr',
    'SCTPMGR_IMG':'registry.gitlab.casa-systems.com/mobility/amf/sctpmgr',
    'GNB_IMG':'registry.gitlab.casa-systems.com/mobility/sim-gnb',
    'NSSF_IMG':'registry.gitlab.casa-systems.com/mobility/sim-nssf',
    'NRF_IMG':'registry.gitlab.casa-systems.com/mobility/sim-nrf',
    'AUSF_IMG':'registry.gitlab.casa-systems.com/mobility/ausf/sim-ausf',
    'AGENT_IMG':'registry.gitlab.casa-systems.com/mobility/nrf/nrf-agent'
    }

start = time.time()
for value in images.values():
    print(value)
    os.system('docker pull {}'.format(value))
    print('pull {} successful!'.format(value))
end = time.time()
print('>>>>>>>>the time now:',datetime.now())
print('>>>>>>>spend time(s):{}'.format(end-start))

