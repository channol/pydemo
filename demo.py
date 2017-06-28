#!/usr/bin/python3
#-*- coding: UTF-8 -*-
#HARD

'''
print('实例1:')
d=[]
for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if i != j != k:
                print(i,j,k)
                d.append([i,j,k])
print('长度:{}'.format(len(d)))
print(d)

print('='*30)
print('实例2:')
#i = int(input('输入净利润:'))
i = int(120000)
arr = [1000000,600000,400000,200000,100000,0]
rat = [0.01,0.015,0.03,0.05,0.075,0.1]
r = 0
for idx in range(0,6):
    if i > arr[idx]:
        r += (i - arr[idx]) * rat[idx]
        print((i - arr[idx]) * rat[idx])
        i = arr[idx]
print (r)

print('='*30)
print('实例3:')
'''

'''
import random

def guess():
    "猜数字!"
    n = int(random.randint(1,100))
#    print(n)
    while True:
        s = input('输入1到100间的数字,输入end退出猜谜:')
        if s == 'end':
            break
        elif not s.isnumeric():
            print('请输入数字!')
            continue
        elif int(s) > n :
            print('输入数字大了!')
        elif int(s) < n :
            print('输入数字小了!')
        else:
            print('答对了!')
            print('底数是: {}'.format(n))
            break
if __name__ == '__main__':
    guess()
   # guess()
'''

import random
#虫子和蚂蚁移动的

class Sprite(object): #父类 精灵类
    step = [-2,+2,-3,+3]

    def __init__(self,gm,point=None):  #生成一个位置
        self.gm = gm
        if point is None:
            self.point = random.randint(0,20)
        else:
            self.point =  point
    def jump(self): #移动方法, 通用
        astep = random.choice(Sprite.step)  #随机产生的移动的大小
        if 0 <= self.point+astep <= 20:
            self.point += astep

class Ant(Sprite):
    def __init__(self,gm,point):
        super(Ant,self).__init__(gm,point)
        self.gm.set_point('ant',self.point) #显示初始化位置
    def jump(self):
        super(Ant, self).jump()
        self.gm.set_point('ant',self.point) #显示移动位

class Worm(Sprite):
    def __init__(self,gm,point):
        super(Worm,self).__init__(gm,point)
        self.gm.set_point('worm',self.point) #显示初始化位置
    def jump(self):
        super(Worm, self).jump()
        self.gm.set_point('worm',self.point) #显示移动位


class GameOver(object): #地图类
    def __init__(self):
        self.ant_point = None
        self.worm_point = None
    def catched(self):
        print('ant:',self.ant_point,'worm:',self.worm_point
        if self.ant_point is not None and self.worm_point is not None and self.ant_point == self.worm_point:
      #      return True
    def set_point(self,tp,point):
        if tp == 'ant':
            self.ant_point = point
        if tp == 'worm':
            self.worm_point = point

if __name__ == '__main__':
    gm = GameOver()
    worm = Worm()
    ant = Ant()