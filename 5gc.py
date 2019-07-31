#!/usr/bin/python3

import sys,re,time,os
import logging
import pexpect

host = '172.0.5.27'
user = 'root'
password = 'casa'

cmd = "ssh "+user+"@"+host
