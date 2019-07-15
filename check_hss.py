#!/usr/bin/python3
#1.定时检测hss进程startup.sh及java是否运行，存在则打印PID
#2.如果其一进程不存在，则kill掉相关进程，重启运行脚本并检测是否成功（同1）
#3.采用crontab方式创建定时任务，/etc/crontab
#*  *    * * *   root    cd /opt/FHoSS/deploy;/usr/bin/python3 checkhss.py >> /root/checkhss.log
#4.注意crontab只会使用默认的环境变量，因此需要在sh脚本上加上相应的环境变量，例如加上：source /etc/profile在sh脚本开头
#5.注意crontab尽量使用绝对路径，并保证用户权限
import psutil
import os
import time
######
def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print('the process {} PID is {}'.format(processname,pid))
           #print(pid)
            break
    else:
        print('***service {} is not found!***'.format(processname))
        return 0

os.system('date')
if (judgeprocess('startup.sh') != 0) and (judgeprocess('java') !=0):
    print('***HSS is running!!***')
else:
    print('***HSS is down!!!!!***')
    print('***restart openHSS!***')
    os.system('pkill -9 startup.sh')
    time.sleep(3)
    os.system('pkill -9 java')
    time.sleep(3)
    os.system('cd /opt/FHoSS/deploy/')
    os.system('nohup ./startup.sh &')
    time.sleep(10)
#    judgeprocess('startup.sh')
#    judgeprocess('java')
    if (judgeprocess('startup.sh') != 0) and (judgeprocess('java') !=0):
        print('***hss-startup restart successful!***')
    else:
        print('***hss can not restart failure!***')
