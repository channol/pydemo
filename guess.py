#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import random

def guess():
    "定义一个guess函数:猜0到100内的数字!先随机一个100内的数字,循环猜谜!"
    n = int(random.randint(1,100)) #100内随机数
    print('=' * 80)
    print('猜数字游戏:输入一个1到100间的整数!输入end退出猜谜!输入help获取谜底!')
    print('=' * 80)
    while True:
        s = input('请输入1到100间的数字(输入end退出,help获取谜底):')
        if s == 'end':  #end退出
            break
        elif s == 'help':  #获取谜底并退出
            print('谜底数是: {}'.format(n))
            break
        elif not s.isnumeric():  #判断是否数字
            print('输入有误!请输入数字!')
            continue            #返回输入提示
        elif int(s) > n:
            print('输入数字大了!')
        elif int(s) < n:
            print('输入数字小了!')
        else:
            print('恭喜您,答对了!')
            print('谜底数是: {}'.format(n))
            break
if __name__ == '__main__':
    guess()