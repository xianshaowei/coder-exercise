#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

20190321  使用类argparser处理参数
20190322  切换到类
20190426  增加功能：支持操作连续IP地址
20190426  增加功能：支持在远程执行本地的脚本

'''

import sys

sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")

import paramiko
import time
import argparse
import os
import re
import shlex
import subprocess
from threading import Thread
from multiprocessing import Process, pool, Queue
import multiprocessing
import random

sys.path.append("/Users/netease/Documents/git/git-201808-newbie-xianwei01/python/")
from pyCommon.network import *
from pyCommon.color import colorPrint
# from pathos.multiprocessing import ProcessingPoll as Pool
from galaxy import Connection

ssh_key = "/Users/netease/.ssh/id_rsa"
file_inventory = subprocess.Popen(["pwd"], stdout=subprocess.PIPE).stdout.read()
remote_inventory = "/home/xianwei01/"


class myconn:
    def __init__(self):
        self.unreach_list = []
        self.color = colorPrint()
        self.unreach_que = Queue()

    # 测试主机连通性
    def nc_port_test(self, host, que):
        '''测试主机是否能够连接'''

        # IP有效性检查和主机名检查
        if not is_valid_ip(host) and re.match('^cld-', host) == None:
            # self.color.redPrint(host , " not a valid ip. or hostname not begin with \'cld-\' ")
            return 1
        port_test_command = "nc  -G 3 -w 1  " + host + " 32200 >/dev/null  2>&1"

        if os.system(port_test_command) == 0:
            return 0
        else:
            # self.color.redPrint(host,'  is unreachable!')
            que.put(host)
            return 1

    # 基本方法
    def root_to_run_oneip_multiline(self, host, command, que):

        if self.nc_port_test(host, que) == 1:
            return 1

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
            # time.sleep(0.05)
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
            shell.close()
            result = buff
        else:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            ssh.close()

        # 返回结果

        res_list = list(result.split('\n'))
        print("\033[1;32;40m%s ----> # %s\033[0m") % (hostname, cmd)

        for i in xrange(0, len(res_list) - 1):
            if i == 0:
                # print("\033[1;32;40m%s\t\t\033[0m") % res_list[i]
                pass
            else:
                print(res_list[i])

        return result

    def root_to_run_oneip_oneline(self, host, command, que):

        hostname = host
        username = 'xianwei01'
        port = 32200
        su_password = 'fai'
        cmd = command

        if self.nc_port_test(host, que) == 1:
            return 1

        private_key = paramiko.RSAKey.from_private_key_file(ssh_key)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname, port, username, private_key, timeout=5)
        except Exception:
            # print ("\033[1;31;40m%s\t\t\033[0m") % hostname  # 红色打印
            return

        if username != 'root':
            shell = ssh.invoke_shell()
            # time.sleep(0.05)
            shell.send('su \n')
            buff = ''
            while not buff.endswith('Password: '):
                resp = shell.recv(999999)
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
            shell.close()
            result = buff
        else:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            ssh.close()

        # 格式化输出
        #print(result)
        res_list = list(result.split('\r\n'))
        # if len(res_list) == len(res_list): print
        alist = []

        alist.append(hostname)
        for i in xrange(1, len(res_list) - 1): alist.append(res_list[i], )

        for i in xrange(len(alist)):
            if i == 0:
                # print("\033[1;32;40m%s\033[0m") % alist[i],
                print alist[i],
                print "-----> ",
            elif i == len(alist) - 1:
                print alist[i]
            else:
                print alist[i],

        return result

    # 远程执行命令
    def root_to_do_ipfile_oneline(self, ipfile, command, que):
        '''对IP列表的IP地址，依次进行执行命令（单进程单线程） '''

        if os.access(ipfile, os.F_OK):
            # print "Given file path is exist."
            pass
        else:
            print
            'The iplist  " %s " is not exist.' % ipfile
            return 1
        iplist = []
        with open(ipfile, "r") as fp:
            for line in fp:
                iplist.append(line.split()[0].strip("\n"))

        # 不使用队列，会出现输出乱序
        process_list = []
        for ip in iplist:
            p = Process(target=self.root_to_run_oneip_oneline, args=(ip, command, que))
            p.daemon = True
            process_list.append(p)

        for p in process_list:
            time.sleep(0.1)
            p.start()
        for p in process_list:
            p.join()

        return

    def root_to_do_ipfile_mulline(self, ipfile, command, que):
        '''对IP列表的IP地址，依次进行执行命令（单进程单线程） '''
        if os.access(ipfile, os.F_OK):
            # print "Given file path is exist."
            pass
        else:
            print
            'The iplist  " %s " is not exist.' % ipfile
            return 1
        iplist = []
        with open(ipfile, "r") as fp:
            for line in fp:
                iplist.append(line.split()[0].strip("\n"))
        # print iplist

        # 获取当前程序名
        # program_name = __file__
        # print program_name
        # cmd = "ps aux |grep -v 'grep' |grep %s " %__file__
        # print os.system(cmd)
        # 不使用队列，会出现输出乱序
        process_list = []
        for ip in iplist:
            p = Process(target=self.root_to_run_oneip_multiline, args=(ip, command, que))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            time.sleep(0.1)
            proc.start()
        for proc in process_list:
            proc.join()
        return 0

        # 使用队列
        # que = Queue.Queue()
        #
        # for ip in iplist:
        #     p = Process(target=root_to_run_mulline, args=(ip, command))
        #     p.daemon = True
        #     que.put(p)
        #
        # while True:
        #     if not que.empty():
        #         proc = que.get(True)
        #         proc.start()
        #         proc.join()
        #     else:
        #         break

    def multi_process_ip_list_multiline(self, ip_string, command, que):
        " 处理连续的IP地址段内段IP地址 -l 1.1.1.1-5,1.1.1.10"

        iplist = deal_ip_list(ip_string)
        self.color.redPrint("The sum of hosts is :  ", len(iplist))
        process_list = []
        for ip in iplist:
            p = Process(target=self.root_to_run_oneip_multiline, args=(ip, command, que))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            time.sleep(0.1)
            proc.start()
        for proc in process_list:
            proc.join()
        return 0

    def multi_process_ip_list_oneline(self, ip_string, command, que):
        " 处理连续的IP地址段内段IP地址 -l 1.1.1.1-5,1.1.1.10"

        iplist = deal_ip_list(ip_string)
        self.color.redPrint("The sum of hosts is :  ", len(iplist))
        process_list = []
        for ip in iplist:
            p = Process(target=self.root_to_run_oneip_oneline, args=(ip, command, que))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            time.sleep(0.1)
            proc.start()
        for proc in process_list:
            proc.join()
        return 0

    # 上传文件
    def upload_file(self, que, host, uploadfile, username='xianwei01', remote_path=remote_inventory,
                    local_path=file_inventory, port=32200):

        if self.nc_port_test(host, que) == 1:
            return 1

        color = colorPrint()
        localfile = local_path.strip() + "/" + uploadfile
        remotefile = remote_path + uploadfile

        if not os.path.exists(localfile):
            print("{filename} is not exist.".format(filename=localfile))
        else:
            print("{filename} is exist.".format(filename=localfile))
        # 创建ssh对象
        private_key = paramiko.RSAKey.from_private_key_file(ssh_key)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, private_key, timeout=5)
        except Exception:
            # print ("\033[1;31;40m%s\t\t\033[0m") % host  # 红色打印
            return

        tran = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(tran)

        try:
            sftp.put(localfile, remotefile)
        except Exception:
            # print("[-]put Error:User name or password error ,pls check")
            error_print = "Upload Error:"
            print("\033[1;31;40m%s \033[0m USERNAME or PASSWORD error,pls check\t") % error_print
            return 1
        color.greenPrint("上传文件完成：", localfile, "    --------->    ", host, remotefile)

        sftp.close()

    def multi_process_to_upload_ipfile(self, ipfile, uploadfile, que):
        '''用多进程实现对多个主机同时 上次文件 '''
        iplist = []
        with open(ipfile, "r") as fp:
            for line in fp:
                iplist.append(line.split()[0].strip("\n"))

        process_list = []
        for ip in iplist:
            p = Process(target=self.upload_file, args=(que,
                                                       ip, uploadfile, 'xianwei01', remote_inventory, file_inventory,
                                                       32200))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            time.sleep(0.1)
            proc.start()
        for proc in process_list:
            proc.join()
        return

    def multi_process_to_upload_iplist(self, ip_string, uploadfile, que):
        '''用多进程实现对多个主机同时 上次文件 '''
        iplist = deal_ip_list(ip_string)

        process_list = []
        for ip in iplist:
            p = Process(target=self.upload_file,
                        args=(que, ip, uploadfile, 'xianwei01', remote_inventory, file_inventory, 32200))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            time.sleep(0.1)
            proc.start()
        for proc in process_list:
            proc.join()
        return

    # ping测试
    def multi_ping(self, host, qu):
        '''ping 一个主机，颜色输出'''
        color = colorPrint()
        ping_test_command = "ping -c 1 -W 2  " + host + " >/dev/null  2>&1"
        ping_test_res_code = os.system(ping_test_command)
        if ping_test_res_code == 0:
            # 如果ping通
            color.greenPrint(host, '   is OK ')
        else:
            # color.redPrint(host, '   is Unreachable.')
            qu.put(host)
            # while not qu.empty():
            #     print qu.get()

    def multi_process_to_multi_ping(self, ipfile, ):
        '''用多进程实现对多个主机同时ping'''
        unreach_host_que = Queue()
        color = colorPrint()
        iplist = []
        with open(ipfile, "r") as fp:
            for line in fp:
                iplist.append(line.split()[0].strip("\n"))

        process_list = []
        for ip in iplist:
            p = Process(target=self.multi_ping, args=(ip, unreach_host_que,))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            proc.start()
        for proc in process_list:
            proc.join()

        while not unreach_host_que.empty():
            print("\033[1;31;40m%s\tis unreachable!\t\033[0m") % unreach_host_que.get()
        return

    def multi_process_to_multi_ping_for_iplist(self, ip_string, ):
        '''用多进程实现对多个主机同时ping'''
        unreach_host_que = Queue()
        color = colorPrint()

        iplist = deal_ip_list(ip_string)
        process_list = []
        for ip in iplist:
            p = Process(target=self.multi_ping, args=(ip, unreach_host_que,))
            p.daemon = True
            process_list.append(p)

        for proc in process_list:
            proc.start()
        for proc in process_list:
            proc.join()

        while not unreach_host_que.empty():
            print("\033[1;31;40m%s\tis unreachable!\t\033[0m") % unreach_host_que.get()
        return

    # 远程执行脚本
    def multi_process_do_script_ip_list_multiline(self, ip_string, uploadfile, que):
        """在远程机器上执行脚本"""
        self.multi_process_to_upload_iplist(ip_string, uploadfile, que)
        command = "bash /home/xianwei01/%s" % uploadfile
        self.multi_process_ip_list_multiline(ip_string, command, que)

    def multi_process_do_script_ip_list_oneiline(self, ip_string, uploadfile, que):
        """在远程机器上执行脚本"""
        self.multi_process_to_upload_iplist(ip_string, uploadfile, que)
        command = "bash /home/xianwei01/%s" % uploadfile
        self.multi_process_ip_list_oneline(ip_string, command, que)

    def multi_process_do_script_ip_file_multiline(self, ipfile, uploadfile, que):
        """在远程机器上执行脚本"""
        self.multi_process_to_upload_ipfile(ipfile, uploadfile, que)
        command = "bash /home/xianwei01/%s" % uploadfile
        self.root_to_do_ipfile_mulline(ipfile, command, que)

    def multi_process_do_script_ip_file_oneiline(self, ipfile, uploadfile, que):
        """在远程机器上执行脚本"""
        self.multi_process_to_upload_ipfile(ipfile, uploadfile, que)
        command = "bash /home/xianwei01/%s" % uploadfile
        self.root_to_do_ipfile_oneline(ipfile, command, que)

    def get_token(self):
        """从auth取token"""
        import requests
        auth_url = "http://auth.nie.netease.com/api/v1/tokens"

        auth_payload = "{\n" \
                       "    \"user\": \"_cld_readonly\",\n" \
                       "    \"key\": \"56972b6fff3e48b7a0edf4ceae58da17\",\n" \
                       "    \"ttl\": 604800" \
                       "\n}"
        auth_headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }
        try:
            auth_response = requests.request("POST", auth_url, data=auth_payload, headers=auth_headers)
        except requests.exceptions.ConnectionError:
            print
            'WARNING:get auth_token faild...'
            return 1
        token = auth_response.json()["token"]
        print
        token
        return token


def main():
    '''
    -i ip
    -f ipfile.txt
    -s excuate a script on remote server
    -l list_ip
    -c upload file from local to remote
    -g get auth token

    :return:
    '''
    main_que = Queue()

    conn = myconn()
    # 实例化一个对象
    par = argparse.ArgumentParser(description='How to use my tool.')
    # 保存参数到namespace
    par.add_argument('--oneline', '-o', default=False, help="special a output in oneline", action="store_true")
    # 保存参数到namespace
    par.add_argument('--copy', '-C', default=False, help="copy file to remote host.", action="store_true")
    # 保存参数到namespace
    par.add_argument('--ping', '-p', default=False, help="ping a host", action="store_true")
    # 指定参数
    par.add_argument('--ip', '-i', type=str, help="special a ip")
    # 指定参数
    par.add_argument('--iplist', '-l', type=str, help="special ips,like: mdo -l10.191.4.13-20 -c\"pwd \" ")
    # 指定参数
    par.add_argument('--ipfile', '-f', type=str, help="special a filename")
    # 指定参数
    par.add_argument('--command', '-c', type=str, help="special a command")
    # 指定参数
    par.add_argument('--script', '-s', type=str, help="excuate a bash script")
    # 指定参数
    par.add_argument('--uploadfile', '-u', type=str, help="special a filename")
    # 指定参数
    par.add_argument('--gettoken', '-t', default=False, help="get token from auth", action="store_true")
    # par.set_defaults(function=sayhi)
    args = par.parse_args()
    # args.function()
    # print args

    if args.ping and args.ipfile == None and args.iplist == None:
        # ping单个主机
        conn.multi_ping(args.ip, main_que)

    elif args.ping and args.ipfile:
        # ping多个主机
        conn.multi_process_to_multi_ping(args.ipfile)

    elif args.ping and args.iplist:
        # ping多个主机
        conn.multi_process_to_multi_ping_for_iplist(args.iplist)

    elif args.ip and args.command:
        # 单个主机执行命令
        conn.root_to_run_oneip_multiline(args.ip, args.command, main_que)

    elif args.ipfile and args.command and args.oneline == False:
        # 批量执行命令，多行输出
        conn.root_to_do_ipfile_mulline(args.ipfile, args.command, main_que)

    elif args.ipfile and args.command and args.oneline:
        # 批量对IP文件执行命令，单行输出
        conn.root_to_do_ipfile_oneline(args.ipfile, args.command, main_que)

    elif args.iplist and args.command and args.oneline == False:
        # 批量对IP列表执行命令， 多行输出
        conn.multi_process_ip_list_multiline(args.iplist, args.command, main_que)

    elif args.iplist and args.command and args.oneline:
        # 批量对IP列表执行命令， 多行输出
        conn.multi_process_ip_list_oneline(args.iplist, args.command, main_que)

        # 单主机上传文件
    elif args.copy and args.ip and args.uploadfile:
        conn.upload_file(main_que, args.ip, args.uploadfile)

        # 批量上次文件
    elif args.copy and args.ipfile and args.uploadfile:
        conn.multi_process_to_upload_ipfile(args.ipfile, args.uploadfile, main_que)

    elif args.copy and args.iplist and args.uploadfile:
        conn.multi_process_to_upload_iplist(args.iplist, args.uploadfile, main_que)

        # 对列表指定对机器执行脚本，多行输出
    elif args.iplist and args.script and args.oneline == False:
        conn.multi_process_do_script_ip_list_multiline(args.iplist, args.script, main_que)

    elif args.iplist and args.script and args.oneline:
        conn.multi_process_do_script_ip_list_oneiline(args.iplist, args.script, main_que)

        # 对文件指定对机器执行脚本，多行输出
    elif args.ipfile and args.script and args.oneline == False:
        conn.multi_process_do_script_ip_file_multiline(args.ipfile, args.script, main_que)

    elif args.ipfile and args.script and args.oneline:
        conn.multi_process_do_script_ip_file_oneiline(args.ipfile, args.script, main_que)

    elif args.gettoken:
        conn.get_token()

    # 最后打印无法联通多机器
    while not main_que.empty():
        print("\033[1;31;40m%s\tIt's 32200 port is unreachable!\t\033[0m") % main_que.get()


if __name__ == "__main__":
    # ans = raw_input("Input \'yes\' or \'no\':")
    # if ans  != 'yes':
    #     print("bye!")
    #     exit(0)
    start_time = time.time()
    main()
    exec_time = int(time.time() - start_time)
    print("It take\033[1;35;40m  %d(s) \033[0m  to do your work. ") % exec_time