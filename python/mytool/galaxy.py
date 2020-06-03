#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import logging
from logging.handlers import WatchedFileHandler
import requests.packages.urllib3.exceptions
import requests
import json

# disable requests verify certification
#from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#定义日志输出

LOGFILE = os.path.expanduser("~/log/galaxy_api.log")
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)
HANDLER1 = logging.StreamHandler(sys.stdout)
#WatchedFileHandler is a kind of filehandler
HANDLER2 = WatchedFileHandler(LOGFILE)
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s",\
                          "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setFormatter(FMTER)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)


path = '/etc/ansible/inventory/'

#定义输出颜色
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NATIVE = '\033[m'


def log_test():
    LOG.info("test")
    LOG.error("test2")

def get_token():
    token = 'eP5qn9kC2cYPiGkns73B17tfgUH2a6anXgWbllMOVQ4u2xo%2Fx4rEt5BpzK92kJD5DLdbKBjjv9XS%0AGnbwcglfvG85vGDyYQfaFxe%2BJszrGWqRRkmx%2FSKmN1%2B%2FvJcKvl6Zd6D%2Fodi7VAXQWDHlCOKfIlIa%0Aao0MEw5QCb1CGjsUu9c%3D%0A'
    return token


class Connection:
    def __init__(self):
        self.token = get_token()
        self.galaxy_url_prefix = 'https://galaxy.nie.netease.com/api/v1/'
        self.dict_gid_to_id ={
            58: 56053
        }

    def get_header(self):
        header = {
            'X-AUTH-PROJECT': 'cld',
            'X-AUTH-TOKEN': self.token,
            'Content-Type': 'application/json'
        }
        return header

    def get(self,resource):
        header = self.get_header()

        #resource = '/groups/6168/ips'
        url = self.galaxy_url_prefix + resource

        r = requests.get(url, headers=header, verify=False)

        if r.status_code in [200, 201, 204, 206]:
            #LOG.info("SUCCESS. Response:");
            try:
                #result = r.text
                result = json.loads(r.text)
                return result
            except ValueError:
                # decoding failed
                pass
            else:
                return None
        else:
            #self.parse_error(r.status_code, r.text)
            return None

    def get_group_ips(self,gid):
        '''获取集群到所以机器IP地址，并写入文件，文件名与集群号一样'''
        group_id = self.get_group_id(gid)
        resource = '/groups/' + str(group_id) + '/ips'
        res = self.get(resource)

        path = '/etc/ansible/inventory/'
        file_name = path + str(gid)

        with open(file_name, "w+") as fp:         #如果文件不存在就删除，读写前会清空文件内容
            for i in res:
                fp.write(i + '\n')
            LOG.info("get group: %s ips done!" %str(gid))

    def get_service_ips(self,gid):
        '''获取给定集群中所有service对应对ip地址或主机名'''
        path = '/etc/ansible/inventory/'
        conn = Connection()
        group_id = self.get_group_id(gid)
        resource = '/groups/' + str(group_id) + '/services'
        res = conn.get(resource)

        service_list = []
        for i in res:
            service_list.append(i['serviceName'])            # 获取所有服务

        for s_name in service_list:
            file_name = path + str(gid) + '-' + s_name      #文件名如 51-docker-node
            with open(file_name, "w+") as fp:
                for i in res:
                    if i['serviceName'] == s_name:
                        for j in i['machines']:
                            #fp.write(j['name'] + '\n')      #获取指定服务对所有机器名
                            fp.write(j['ip'] + '\n')       #获取指定服务对所有机器IP
            LOG.info("%s have done!" %s_name)
        return 0

    def get_group_id(self,gid):
        ''' 通过gid获得group_id'''
        conn = Connection()
        #group_dict = self.get_allGroupIP()
        group_dict = {}
        res = conn.get('groups?_opt=1&_num=-1')
        for i in res['items']:
            # print i['gid'], i['id'], i['groupName']
            if i['gid'] not in group_dict.keys():
                group_dict[i['gid']] = [i['id'], i['groupName']]
        return group_dict[str(gid)][0]

    def get_allGroupIP(self):
        '''获取所有集群，对应的所有机器IP'''
        conn = Connection()
        group_dict = {}
        res = conn.get('groups?_opt=1&_num=-1')
        for i in res['items']:
            # print i['gid'], i['id'], i['groupName']
            if i['gid'] not in group_dict.keys():
                group_dict[i['gid']] = [i['id'], i['groupName']]
        for key, val in group_dict.iteritems():  # 遍历
            self.get_group_ips(key)
            self.get_service_ips(key)
        return 0

    def get_allServiceIP(self):
        '''获取所有集群，对应所有服务，的所有机器IP'''
        pass
        return 0

def main():
    log_test()
    conn = Connection()
    #print conn.get('/groups/6168/ips')
    #res =  conn.get('/groups')
    #res = conn.get('/groups/56053/ips')     #狐狸座
    #print res['items']
    #print type(res)
    #for i in res['items']:
        #print i['gid'], i['id'], i['groupName']    #获取gid
     #   print i
    #print res

    #conn.get_group_ips(9352)
    #孔雀座52065
    #conn.get_group_ips(1001)

    #获取所有集群对IP
    conn.get_allGroupIP()
    # !/usr/bin/python
    # -*- coding: UTF-8 -*-

    #写入dict
    # group_dict = {}
    # res = conn.get('groups?_opt=1&_num=-1')
    # for i in res['items']:
    #     #print i['gid'], i['id'], i['groupName']
    #     if i['gid'] not in group_dict.keys():
    #         group_dict[i['gid']] = [i['id'],i['groupName']]
    #
    #     #print i
    # for k, v in group_dict.iteritems():  # 遍历
    #     print k, v



    #get service ip
    # res = conn.get('groups/52065/services')
    # for i in res:
    #     #print i
    #     #print i['gid'], i['id'], i['groupName']
    #     print i['serviceName']                     #获取所有服务
    #     # if i['serviceName'] == 'API-Server' :
    #     #     #print type(i['machines'])
    #     #     for j in  i['machines']:
    #     #         print j['name'],j['ip']
    #conn.get_service_ips(51)

if __name__=='__main__':
    main()