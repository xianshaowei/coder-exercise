#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

20190321  使用类argparser处理参数
20190322  切换到类
20190426  增加功能：支持操作连续IP地址
20190426  增加功能：支持在远程执行本地的脚本

'''

import sys
sys.path.insert(0,"/usr/local/lib/python2.7/site-packages/")

import paramiko
import time
import argparse
import os
import re
import shlex
import subprocess
from threading import Thread
from multiprocessing import Process,pool,Queue
import multiprocessing
import random
sys.path.append("/Users/netease/Documents/git/git-201808-newbie-xianwei01/python/")
from pyCommon.network import  *
from pyCommon.color import colorPrint
#from pathos.multiprocessing import ProcessingPoll as Pool


ssh_key = "/Users/netease/.ssh/id_rsa"

def root_to_run_oneip_multiline(host, command, que):

    color = colorPrint()
    hostname = host
    username = 'xianwei01'
    port = 32200
    su_password = 'fai'
    cmd = command

    private_key = paramiko.RSAKey.from_private_key_file(ssh_key)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, port, username, private_key, timeout=5)
    except Exception:
        # print ("\033[1;31;40m%s\t\t\033[0m") % hostname  # 红色打印
        return 1

    if username != 'root':
        shell = ssh.invoke_shell()
        shell.send('su  \n')
        buff = ''
        while not buff.endswith('Password: '):
            resp = shell.recv(999)
            buff += resp
        shell.send(su_password)  # su to root
        shell.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = shell.recv(999999)
            buff += resp
        shell.send(cmd)  # exec command
        shell.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = shell.recv(999999)
            buff += resp
        result = buff
    else:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
    #time.sleep(0.2)
    shell.close()

    return result

def multi_process_pool_do_ssh(iplist,command,que):

    res_list = []
    pool = multiprocessing.Pool(processes=5)
    for i in iplist:
        res = pool.apply_async(root_to_run_oneip_multiline,(i,command,que))
        res_list.append(res)
    for r in res_list:
        print r.get()


def main():
    # host = '10.202.10.12'
    command = 'route -n'
    que = Queue()
    # root_to_run_oneip_multiline(host, command, que)
    iplist = ['10.202.10.12', '10.202.10.13', '10.202.10.14']
    m = multiprocessing.Manager()
    que = m.Queue()
    multi_process_pool_do_ssh(iplist,command,que)

if __name__ == "__main__":
    main()