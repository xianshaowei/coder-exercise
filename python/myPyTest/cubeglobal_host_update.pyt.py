#!/usr/bin/env python
# -*- coding:utf8 -*-

import requests
import httplib
import json
import time,os,sys


cube_global1_ip = '10.160.112.62'
cube_global2_ip = '10.160.112.63'


lbc_url_test = 'http://lbcapi-test.nie.netease.com:10086'
lbc_url = 'http://lbcapi-in.nie.netease.com:8080'
auth_body = {
    "user": "_cld_readonly",
    "key": "56972b6fff3e48b7a0edf4ceae58da17",
    "ttl": 7200
        }
auth_header= {
    'Content-Type': 'application/json'
}
auth_url = 'http://auth.nie.netease.com/api/v1/tokens'

result = requests.post(auth_url, headers=auth_header, json=auth_body)
datas = result.json()
galaxy_token = datas['token']

header = {
            'X-Auth-Token': galaxy_token,
            'X-Auth-Project': 'cld',
            'Content-Type': 'application/json'
        }

# port对应LBC"端口配置中的端口"
# project对应一个instance

'''
# 通过instance名获取port id
#projectid = '6514'      #对应cld-apisvr2-1009
#cube_realserver = '/project/6514/ports'
cube_realserver = '/project/@cube-global-test/ports'
url = lbc_url + cube_realserver
result = requests.get(url, headers=header)
datas = result.json()
print datas
ports = datas['items']
for port in ports:
   if port['portnum'] == 19090:
       id = port['id']
print "port id: %d" %id

# port url
port_url = '/port/%s/realservers' % id

# port 下的内容：即包括哪些realsvr
url = lbc_url + port_url
result = requests.get(url, headers=header)
datas = result.json()
print datas['items']

# 获取realserver id
realservers = datas['items']
realsvr_id = []
for r in realservers:
    realsvr_id.append(r['id'])

print realsvr_id
'''



def run(cmd):
    """ Run a shell command and return its output."""
    import subprocess
    proc = subprocess.Popen(cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    (stdoutput, erroutput) = proc.communicate()
    if proc.returncode == 0:
        finish_run = True
    else:
        finish_run = False

    return (finish_run, stdoutput.strip(), erroutput.strip())

def get_portid(projectname,portname):
    '''通过projectname也就是实例名获取19090端口对应的port id'''
    port_url_suff = '/project/@%s/ports' %projectname
    port_url = lbc_url + port_url_suff
    try:
        result = requests.get(port_url, headers=header)
    except Exception as e:
        raise Exception("get ports from LBC fail")
    if not str(result.status_code).startswith('20'):
        print("%s: %s" % (result.status_code, result.text))
        exit(1)
    datas = result.json()
    ports = datas['items']
    for port in ports:
        if port['portnum'] == portname:
            id = port['id']
    print "port id: %d" % id
    return id


def get_realserver_ids(portid):
    '''获取port下的内容：即包括哪些realsvr'''
    realservers_url_suff = '/port/%s/realservers' % portid
    rsvrs_url = lbc_url + realservers_url_suff
    try:
        result = requests.get(rsvrs_url, headers=header)
    except Exception as e:
        raise Exception("get realservers from LBC fail")
    if not str(result.status_code).startswith('20'):
        print("%s: %s" % (result.status_code, result.text))
        exit(1)
    datas = result.json()

    # 获取realserver id
    realservers = datas['items']
    realsvr_id = []
    for r in realservers:
        realsvr_id.append(r['id'])

    print realsvr_id
    return realsvr_id



def change_realsvr_weight(realserver_id, weight):
    '''修改realserver的weight属性'''
    rsvr_url_suff = '/realservers/%s' %realserver_id
    rsvr_url = lbc_url + rsvr_url_suff
    body = {
        "weight": weight
    }
    try:
        result = requests.put(rsvr_url, headers=header, json=body)
    except Exception as e:
        raise Exception("put realserver weight from LBC fail")
    if not str(result.status_code).startswith('20'):
        print("%s: %s" % (result.status_code, result.text))
        exit(1)
    datas = result.json()
    print datas
    return datas


def update_cubeglobal(cubeglobal_ip,rsvr_id):

    # cube-global的weight设置为0
    portid = get_portid("cube-global-test", 19090)
    rsvrid_list = get_realserver_ids(portid)
    if len(rsvrid_list) != 2:
        print("LBC of cube-global is abnormal!")
        exit(1)
    cube_global_svr = rsvrid_list[rsvr_id]          # cubeglobal对应的server_id
    change_realsvr_weight(cube_global_svr, 0)

    # 更新版本
    res_code, res, res_err = run("""
    
     if [ `sudo ifconfig |grep inet |grep %s|wc -l` -eq 1 ];then
        sudo docker-compose -f /home/cld/conf/cube/cubeglobal.yaml down' && \
        sudo docker-compose -f /home/cld/conf/cube/cubeglobal.yaml up -d' 
     fi
     
     """ %(cubeglobal_ip) )
    if res_code == True:
        print res

    # cube-global的weight设置为10
    change_realsvr_weight(cube_global_svr, 10)



def main():
    get_portid("cube-global-test", 19090)

    portid = get_portid("cube-global-test", 19090)
    rsvrid_list = get_realserver_ids(portid)

    if len(rsvrid_list) != 2:
        print("LBC of cube-global is abnormal!")
        exit(1)
    cube_global1_id = rsvrid_list[0]
    cube_global2_id = rsvrid_list[1]

    change_realsvr_weight(cube_global1_id, 0)
    change_realsvr_weight(cube_global2_id, 1)

    netcard = "en4"
    res_code,res,res_err = run("""
                               ifconfig %s
                               who
                               ls     """
                                %netcard)
    if res_code == True:
        print res



if __name__ == "__main__":
    main()
