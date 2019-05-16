#!/usr/bin/python3 

import requests
import re

line = "Catsaresmarterthandogs ar"
print (re.match('ar',line,re.I))

url='https://www.baidu.com'
r=requests.get(url)
r.encoding=r.apparent_encoding
print(r.text[-200:])
print('good1234!')