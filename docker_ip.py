#!/usr/bin/python3

#-*- coding:utf-8 -*-

import paramiko
import sys

cmd = "docker inspect --format='{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)"

if len(sys.argv) != 2:
    print("Usage:\n", sys.argv[0] +" ip")
else:
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=sys.argv[1], port=22, username='root', password='casa')
    print("Login on:", sys.argv[1])
    print("Exec cmd:", cmd)
    print("-----------------")
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    print(result.decode())
    # 关闭连接
    ssh.close()

