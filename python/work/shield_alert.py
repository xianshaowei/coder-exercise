#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import argparse
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 设置galaxy的url和token信息
GALAXY_URL = 'https://galaxy.nie.netease.com/api/v1'
HEADERS = {
                'X-Auth-Token': 'PcoBzJ6fNM7NkKMuFmjxQq5T1z4GwvXeeUMfG0w%2F8XdLTaWtj28Z6PTXVlx%2FoqWqL45I3KPSCy0q%0AjlcXPMvJ8CVdHNeyM%2FwiKimztZFN1G9%2BbeuFRlJH%2FxoIW5yejG9nXvwRs9mVNj0WNWNMjs5t9zTV%0AnTjvpRy1xMOuEd%2BiW88%3D%0A',
                'X-Auth-Project' : 'cld'
                }

def get_machine_hostname_by_ip(ip):
    '''
    通过galaxy使用ip地址查找hostname
    :param ip: ip地址
    :return:
    '''
    request_url = GALAXY_URL + '/machines?_ip=%s' % ip
    result = requests.get(request_url, headers=HEADERS, verify=False)
    datas = result.json()
#    print datas
#    if not datas['items'][0]['name'] :
#        print   datas
    return datas['items'][0]['name']


def shield_alert(hostname_list, desc, ttl):
    '''
    屏蔽monitor报警
    :param hostname_list:
    :param desc:
    :param ttl:
    :return:
    '''
    body = {
        "desc": desc,
        "hosts": hostname_list,
        "start": int(time.time()),
        "ttl": ttl
    }
    monitor_headers = {
        # 最好换一下自己的auth token，这样monitor上面显示的屏蔽记录就会记录是谁做的屏蔽操作
        'X-AUTH-TOKEN': 'PcoBzJ6fNM7NkKMuFmjxQq5T1z4GwvXeeUMfG0w%2F8XdLTaWtj28Z6PTXVlx%2FoqWqL45I3KPSCy0q%0AjlcXPMvJ8CVdHNeyM%2FwiKimztZFN1G9%2BbeuFRlJH%2FxoIW5yejG9nXvwRs9mVNj0WNWNMjs5t9zTV%0AnTjvpRy1xMOuEd%2BiW88%3D%0A',
        'X-AUTH-PROJECT': 'cld'
    }
    url = "http://bh.web.nie.netease.com:7000/api/v1/shield/add"
    resp = requests.post(url=url, headers=monitor_headers, json=body)
    print resp.json()

def split_list(big_list):
    '''
    monitor一次最多支持25台host进行屏蔽
    将大于23台的主机列表进行分割，每个子列表长度为23
    '''
    print 'number of shield host : %s'%(len(big_list))
    sub_list_max_length = 23
    list_in_list = []
    sub_list = []
    for obj in big_list:
        if len(sub_list) < sub_list_max_length:
            sub_list.append(obj)
        elif len(sub_list) >= sub_list_max_length:
            #print len(sub_list)
            list_in_list.append(sub_list)
            sub_list = []
            sub_list.append(obj)
    list_in_list.append(sub_list)
    return list_in_list

def ip2num(ip):
    #将ip地址按照每个8位进行分割，转换为整数
    ips = [int(x) for x in ip.split('.')]
    return ips[0]<< 24 | ips[1]<< 16 | ips[2] << 8 | ips[3]

def num2ip (num):
    #将数字转换成ip地址
    return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))
    #return '%s.%s.%s.%s' % ((num & 0xff000000)>>24,(num & 0x00ff0000)>>16,(num & 0x00000ff00)>>8,num & 0x000000ff)

def time2sec(shielding_time):
    #将时间转换成秒，支持d、m、s
    if shielding_time.find('d') != -1:
        shielding_time = shielding_time.replace('d','')
        sec = int(shielding_time) * 24 * 60 * 60
    elif shielding_time.find('h') != -1:
        shielding_time = shielding_time.replace('h','')
        sec = int(shielding_time) * 60 * 60
    elif shielding_time.find('m') != -1:
        shielding_time = shielding_time.replace('m','')
        sec = int(shielding_time) * 60
    else:
        sec = shielding_time
    return int(sec)



def gen_ip(ip):
    '''
    转换输入的ip地址，支持单个ip及ip列表扩展类型：
    192.168.1.2
    192.168.1.2-10：192.168.1.2-192.168.1.10
    192.168.1.2-168.2.10：192.168.1.2-192.168.2.10
    192.168.1.2-192.168.3.10
    '''
    if ip.find('-') != -1:
        ip_split = ip.split('-')
        ip_split_start = ip_split[0].split('.')
        ip_split_end = ip_split[1].split('.')
        if len(ip_split_start) > len(ip_split_end):
            ip_split_end_tmp = ip_split_start[:]
            delta = len(ip_split_start) - len(ip_split_end)
            for i in range(0,delta):
                ip_split_end.insert(0,'0')
            for i, j in enumerate(ip_split_end):
                if j != '0':
                    ip_split_end_tmp[i] = j
            ip_split_end = ip_split_end_tmp
        ip_split_start = '.'.join(ip_split_start)
        ip_split_end = '.'.join(ip_split_end)
        start ,end = [ip2num(x) for x in [ip_split_start, ip_split_end]]
        return [num2ip(num) for num in range(start,end+1) if num & 0xff]
    elif ip.find('-') == -1:
        ips = []
        ips.append(ip)
        return ips


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--file', '-f', default=False, help="shield_hosts in ./shield_hosts,one host a line", action="store_true")
    group.add_argument('--ips', '-i', type=str, help="ip_list (192.168.1.1-4)")
    parser.add_argument('--time', '-t', type=str, help="support s m h d")
    parser.add_argument('--reason', '-r', type=str, default='maintenance', help="input shield alarm reason", nargs='?')
    parser.add_argument('--debug', '-d', default=False, help="switch on debug mode, print ascript.", action="store_true")
    args = parser.parse_args()
    if args.file:
        if os.path.isfile("shield_hosts"):
            ips = []
            # 修改一下这个文件的内容，里面记录的是需要屏蔽那些ip地址
            fd = open('./shield_hosts', 'r')
            for host in fd.readlines():
                ips.append(host.strip())
        else:
            print "You should create a file named shiel_hosts and listing hosts in it."
            return
    elif args.ips:
        ips = gen_ip(args.ips)
    hostname_list = []
    for ip in ips:
        hostname_list.append(get_machine_hostname_by_ip(ip))
    list_in_list = split_list(hostname_list)
    shielding_time = time2sec(args.time)
    if args.debug:
        print 'sheid_ip list:'
        print '\n'.join(ips)
        print 'sheild host name:'
        print '\n'.join(hostname_list)
        print 'shielding time:'
        print args.time + '--->' + str(shielding_time) + 'sec'
        print 'reason:%s'%(args.reason)
        return
    for sub_list in list_in_list:
        shield_alert(sub_list, args.reason, shielding_time)


if __name__ == "__main__":
    main()