#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time

iplist = []
with open("iplist.txt", "r") as fp:
    for line in fp:
        iplist.append(line.split()[0].strip("\n"))

print(iplist)