#!/usr/bin/python
#coding:utf-8
#
#   Author  :   herry & hxfn1692
#   E-mail  :   hxfn1692@corp.netease.com
#   Date    :   2016/02/23 10:23:55
#   Desc    :   galaxy_api for
#               1. import new VM
#               2. update VM host
#               3. query VM host
#               4. update host IP
#               5. add host IP
#               6. add host desc
#               7. update host desc
#               8. To be added...
#   Usage   :   python rabbitmq_connection_check.py [-b|--blackhole]
#               -b|--blackhole    Post warning to galaxy,disabled by default
#   Notice  :   This script should be running as root at compute manager node
#   Update  :   2016.04.1  (1). remove default token, need to be added by user
#               2016.04.21 (1). add cross project delete vm
#               2016.04.27 (1). fix spotlight API url
#               2016.07.22 (1). add load TOKEN function by igi

import sys
import os
from logging.handlers import WatchedFileHandler
import json
import logging
import requests
import argparse
import socket
import ast

# disable requests verify certification
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests.packages.urllib3.exceptions
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

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


def load_TOKEN():
    '''read TOKEN from file "TOKEN" if exist'''
    if os.path.isfile('TOKEN'):
        TOKEN = open('TOKEN').read().strip()
        return TOKEN
    else:
        return ""

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

class Connection:
    '''
    Connection with galaxy by 4 different methods
    '''
    def __init__(self):
        '''
        init TOKEN and BASE URL
        '''
        # ************* TOKEN to be added by user ***************
        self.TOKEN = ""
        if not self.TOKEN:
            self.TOKEN = load_TOKEN()

        #self.URL = 'http://192.168.34.89:8081/api/v1'
        #self.URL = 'https://play-galaxy.x.netease.com/api/v1'
        #self.BLL_URL = 'https://play-galaxy.x.netease.com/api/v1/bll'
        #self.URL = 'https://galaxy2.x.netease.com/api/v1'
        self.URL = 'https://galaxy.nie.netease.com/api/v1'
        self.BLL_URL = 'https://galaxy.nie.netease.com/api/v1/bll'


    def parse(self, r):
        '''
        parse galaxy return info
        '''
        if r.status_code in [200, 201, 204, 206]:
            LOG.info("SUCCESS. Response:");
            try:
                result = json.loads(r.text)
                return result
            except ValueError:
                # decoding failed
                pass
            else:
                return None
        else:
            self.parse_error(r.status_code, r.text)
            return None

    def parse_error(self, status_code, text):
        '''
        parse detail return error
        '''
        conv_text = ""
        try:
            result = json.loads(text)
            conv_text = json.dumps(result, indent=4).decode('unicode-escape')
        except ValueError:
            # decoding faild
            pass
        if status_code == 400:
            LOG.error("status_code = %s " % status_code + ": Failed")
            LOG.error("text = " + conv_text)
        elif status_code == 401:
            LOG.error("status_code = %s " % status_code + ": Verification Failed")
            LOG.error("text = " + conv_text)
        elif status_code == 403:
            LOG.error("status_code = %s " % status_code + ": Forbidden")
            LOG.error("text = " + conv_text)
        elif status_code == 404:
            LOG.error("status_code = %s " % status_code + ": Not Found")
            LOG.error("text = " + conv_text)
        elif status_code == 409:
            LOG.error("status_code = %s " % status_code + ": Already exist")
            LOG.error("text = " + conv_text)
        elif status_code == 500:
            LOG.error("status_code = %s " % status_code + ": Internal Error")
            LOG.error("text = " + conv_text)
        elif status_code == 503:
            LOG.error("status_code = %s " % status_code + ": Server is busy")
            LOG.error("text = " + conv_text)
        else:
            LOG.error("status_code = %s " % status_code + ": Unkown Error")
            LOG.error("text = " + conv_text)

    def post(self, url, data=None, headers={}):
        '''
        post method for galaxy api
        '''
        url = self.URL + url
        _headers = {
            'X-AUTH-TOKEN': self.TOKEN
        }
        _headers.update(headers)
        r = requests.post(url, json=data, headers=_headers, verify=False)
        LOG.info("POST : %s" % url)
        LOG.info("data = " + json.dumps(data, indent=4).decode('unicode-escape'))
        return self.parse(r)

    def delete(self, url, data=None, headers={}):
        '''
        delete method for galaxy api
        '''
        url = self.URL + url
        _headers = {
            'X-AUTH-TOKEN': self.TOKEN
        }
        _headers.update(headers)
        r = requests.delete(url, json=data, headers=_headers, verify=False)
        LOG.info("DELETE : %s" % url)
        LOG.info("data = " + json.dumps(data, indent=4))
        return self.parse(r)

    def put(self, url, data=None, headers={}):
        '''
        put method for galaxy api
        '''
        url = self.URL + url
        _headers = {
            'X-AUTH-PROJECT':'cld',
            'X-AUTH-TOKEN': self.TOKEN,
            'Content-Type':'application/json'
        }
        _headers.update(headers)
        r = requests.put(url, json=data, headers=_headers, verify=False)
        LOG.info("PUT : %s" % url)
        LOG.info("data = " + json.dumps(data, indent=4))
        return self.parse(r)

    def get(self, url, params=None, headers={}, bll=False):
        '''
        get method for galaxy api
        '''
        if bll == False:
            url = self.URL + url
        else:
            url = self.BLL_URL + url
        _headers = {
            'X-AUTH-PROJECT':'cld',
            'X-AUTH-TOKEN':self.TOKEN,
            'Content-Type':'application/json'
        }
        _headers.update(headers)
        r = requests.get(url, params=params, headers=_headers, verify=False)
        LOG.info("GET : %s" % url)
        return self.parse(r)

    def get_users_test(self):
        params = {
            '_num' : 2,
            '_page' : 1,
        }
        return self.get('/users', params)

def parse_args():
    '''
    parse args for galaxy_api command line
    '''
    parser = argparse.ArgumentParser(description="GALAXY API")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0', help="galaxy api verison")
    #parser.add_argument('-T', '--test', action='store_true',
    #                    help="test galaxy by get users")



    subparsers = parser.add_subparsers(help="galaxy api function list")
    parser_import_vm = subparsers.add_parser('import_vm', help="import vm to \
                                             galaxy project")
    parser_import_vm.add_argument('-p', '--project', required=True,
                                  help="project vm to be imported to")
    parser_import_vm.add_argument('-t', '--type', type=int, choices=range(0,5),
    default=3, help="machine type, default owncloud vm",
    metavar="0:physics machines; 1:VM; 2:external machines; 3:owncloud vm(default); 4:AWS vm")
    parser_import_vm.add_argument('-m', '--vm', required=False,
                                  help="vm ip address")
    parser_import_vm.add_argument('-s', '--host', required=False,
                                  help="host ip address")
    parser_import_vm.add_argument('-f', '--file', required=False,
                                  help="<vm>:<host> each line in a file")
    parser_import_vm.set_defaults(func=import_vm)


    parser_update_vm = subparsers.add_parser('update_vm', help="update vm host\
                                             ip address")
    parser_update_vm.add_argument('-m', '--vm', required=True,
                                  help='vm ip address to be updated')
    parser_update_vm.add_argument('-s', '--host', required=True,
                                  help='vm ip new host to be updated')
    parser_update_vm.set_defaults(func=update_vm)



    parser_query_vm = subparsers.add_parser('query_vm', help="query vm host \
                                             ip address")
    parser_query_vm.add_argument('-n', '--name', required=True,
                                 help="according info query vm, usually ip address")
    parser_query_vm.add_argument('-a', '--all', action='store_true', default=False,
                                 help="all detail info about ip")
    parser_query_vm.set_defaults(func=query_vm)
    parser_delete_vm = subparsers.add_parser('delete_vm', help="delete vm \
                                             in galaxy project")
    parser_delete_vm.add_argument('-i', '--ip', required=True,
                                  help="delete vm by ip address")
    parser_delete_vm.set_defaults(func=delete_vm)
    parser_query_ip = subparsers.add_parser('query_ip', help="query ip address \
                                            info")
    parser_query_ip.add_argument('-i', '--ip', required=True,
                                 help="ip address to query")
    parser_query_ip.set_defaults(func=query_ip)
    parser_add_ip = subparsers.add_parser('add_ip', help="add ip address to \
                                          to machine")
    parser_add_ip.add_argument('-s', '--host', required=True,
                               help="host to add ip")
    parser_add_ip.add_argument('-i', '--ip', required=True,
                               help="ip address to add")
    parser_add_ip.add_argument('-t', '--type', type=int, choices=range(0,3),
    default=1, help="ip type, default slave ip",
    metavar="0:main ip; 1:slave ip(default); 2:internal ip")
    parser_add_ip.set_defaults(func=add_ip)
    parser_update_ip = subparsers.add_parser('update_ip', help="update host ip")
    parser_update_ip.set_defaults(func=update_ip)
    parser_delete_ip = subparsers.add_parser('delete_ip', help="delete host ip")
    parser_delete_ip.add_argument('-s', '--host', required=True,
                                  help="host to delete ip")
    parser_delete_ip.add_argument('-i', '--ip', required=True,
                                  help="ip address to delete")
    parser_delete_ip.set_defaults(func=delete_ip)
    parser_add_desc = subparsers.add_parser('add_desc', help="add description\
                                            to machine")
    parser_add_desc.set_defaults(func=add_desc)
    parser_update_desc = subparsers.add_parser('update_desc', help="update \
                                               description of machine")
    parser_update_desc.set_defaults(func=update_desc)
    parser_test_users = subparsers.add_parser('test', help="test galaxy \
                                               api by get users")
    parser_test_users.set_defaults(func=test_users)

    return parser.parse_args()

def import_vm(conn, args):
    project = args['project'].lower()
    vm_ip = args['vm']
    host_ip = args['host']
    f = args['file']
    vm_type = str(args['type'])
    if vm_ip == None and host_ip == None and f == None:
        LOG.warning("No ip address to import")
        sys.exit(0)
    if f != None:
        LOG.info("import vm ip from file: %s" % f)
        with open(f, 'rb') as fp:
            for line in fp:
                line = line.strip()
                if line == "":
                    continue
                _ = line.split(":")
                LOG.info(_)
                if len(_) < 2:
                    LOG.error("Error: %s" % line)
                    continue
                _ip, _hostip = _[:2]
                _data = {
                    "ips": [_ip],
                    "machineType": vm_type,
                    "parent_ip": _hostip
                }
                result = conn.post('/machines', data=_data,
                                   headers={"X-AUTH-PROJECT" : project})
                LOG.info("import vm %s:%s to project %s"
                         % (_ip, _hostip, project))
                LOG.info(json.dumps(result, indent=4).decode('unicode-escape'))
    if vm_ip == None and host_ip == None and f != None:
        LOG.info("import from file %s done." % f)
        sys.exit(0)
    if vm_ip == None or host_ip == None:
        LOG.error("one of vm ip or host ip is None")
        sys.exit(1)
    if is_valid_ipv4_address(vm_ip) and \
        is_valid_ipv4_address(host_ip):
        _data = {
                 "ips" : [vm_ip],
                 "machineType" : vm_type,
                 "parent_ip" : host_ip
                 }
        LOG.info("import vm %s:%s to project %s" % (vm_ip, host_ip, project))
        result = conn.post('/machines', data=_data,
                           headers={"X-AUTH-PROJECT" : project})
        LOG.info(json.dumps(result, indent=4).decode('unicode-escape'))
    else:
        LOG.error("ip address %s or %s not valid" % (vm_ip, host_ip))

def update_vm(conn, args):
    '''
    update vm host ip
    '''
    vm_ip = args['vm']
    host_ip = args['host']
    if is_valid_ipv4_address(vm_ip) and is_valid_ipv4_address(host_ip):
        vm_r = query_vm(conn, {'name' : vm_ip, 'all' : False})
        host_r = query_vm(conn, {'name' : host_ip, 'all' : False})
        if vm_r == [] or host_r == []:
            LOG.error("no vm % or host %s in galaxy")
            sys.exit(1)
        else:
            vm_id = vm_r[0]['id']
            host_id = host_r[0]['id']
            vm_project = vm_r[0]['project']['projectCode']
            url = '/machines/' + vm_id + '/host/' + host_id
            headers={'X-AUTH-PROJECT': vm_project}
            r = conn.put(url, headers=headers)
            LOG.info(json.dumps(r, indent=4).decode('unicode-escape'))
    else:
        LOG.error("ip address %s or %s not valid" % (vm_ip, host_ip))


def query_vm(conn, args):
    '''
    query vm info
    '''
    name = args['name']
    result = conn.get('/machines/spotlight', params={'name':name}, bll=True)
    if result == []:
        LOG.info("no %s in galaxy" % name)
        sys.exit(0)
    for i in result:
        tmp = {}
        if 'parent_id' in i:
            tmp['name'] = i['name']
            tmp['ip'] = i['ip']
            tmp['ip_internal'] = i['ip_internal']
            tmp['machineType'] = i['machineType']
            tmp['description'] = i['description']
            #tmp['groups'] = i['groups']
            tmp['project'] = i['project']
            tmp['id'] = i['id']
            if i['parent_id'] != None and i['parent_id'] != "0":
                url = "/machines/" + i['parent_id']
                r = conn.get(url)
                LOG.info("获取虚机宿主信息:")
                LOG.info(json.dumps(r, indent=4).decode('unicode-escape'))
                if r != None:
                    tmp["parent_host"] = r['ip']
        LOG.info("获取汇总信息:")
        if 'parent_host' in tmp:
            i["parent_host"] = tmp["parent_host"]
        if args['all'] == True:
            LOG.info(json.dumps(i, indent=4).decode('unicode-escape'))
        else:
            LOG.info(json.dumps(tmp, indent=4).decode('unicode-escape'))
    return result


def delete_vm(conn, args):
    '''
    delete vm from galaxy
    '''
    name = args['ip']
    r = query_vm(conn, {'name' : name, 'all' : False})
    if r == []:
        LOG.error("no %s in galaxy" % name)
        sys.exit(1)
    for i in r:
        if make_sure_yes_or_no("Are you sure delete vm %s" % i['ip']):
            vm_id = i['id']
            url = '/machines/' + vm_id
            project = i['project']['projectCode']
            conn.delete(url, headers={"X-AUTH-PROJECT" : project})
        else:
            LOG.info("choose not delete vm.")


def query_ip(conn, args):
    '''
    query ip address info
    '''
    ips = args['ip']
    url = "/ips"
    params = {
            "_match" : ips
            }
    r = conn.get(url, params)
    LOG.info("获取IP信息:")
    LOG.info(json.dumps(r, indent=4).decode('unicode-escape'))
    return r


def add_ip(conn, args):
    '''
    add ip address to machine
    '''
    host_ip = args['host']
    aip = args['ip']
    ip_type = str(args['type'])
    if not (is_valid_ipv4_address(host_ip) and \
            is_valid_ipv4_address(aip)):
        LOG.error("host ip %s or add ip %s is not valid ip address" %
                  (host_ip, aip))
        sys.exit(1)
    r = query_vm(conn, {'name' : host_ip, 'all' : False})
    if r == []:
        LOG.error("no %s in galaxy" % host_ip)
        sys.exit(1)
    host_id = r[0]['id']
    url = "/machines/" + host_id + "/ips"
    _data = {
             "ip" : aip,
             "ipType" : ip_type,
             "description" : "使用中"
            }
    project = r[0]['project']['projectCode']
    res = conn.post(url, headers={"X-AUTH-PROJECT" : project}, data=_data)
    LOG.info(json.dumps(res, indent=4).decode('unicode-escape'))

def update_ip(conn, args):
    pass

def delete_ip(conn, args):
    '''
    delete ip address from machine
    '''
    host_ip = args['host']
    del_ip = args['ip']
    if not is_valid_ipv4_address(host_ip):
        LOG.error("host ip %s is not valid ip address" % host_ip)
        sys.exit(1)
    r = query_vm(conn, {'name' : host_ip, 'all' : False})
    if r == []:
        LOG.error("no %s in galaxy" % host_ip)
        sys.exit(1)
    host_id = r[0]['id']
    project = r[0]['project']['projectCode']
    res_ip = query_ip(conn, {'ip' : del_ip})
    for i in res_ip['items']:
        if make_sure_yes_or_no("Are you sure delete ip %s" % i['ip']):
            ip_id = i['id']
            url = '/machines/' + host_id + "/ips/" + ip_id
            conn.delete(url, headers={"X-AUTH-PROJECT" : project})
        else:
            LOG.info("choose not delete ip")


def add_desc(conn, args):
    pass

def update_desc(conn, args):
    pass

def test_users(conn, args):
    r = conn.get_users_test()
    LOG.info(json.dumps(r, indent=4).decode('unicode-escape'))

def is_valid_ipv4_address(address):
    '''
    validate ipv4 address
    '''
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def make_sure_yes_or_no(question, default='no'):
    '''
    make sure prompt
    '''
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(bcolors.WARNING + question + prompt +bcolors.NATIVE)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main():
    args = parse_args()
    conn = Connection()
    if conn.TOKEN == "":
        LOG.error("Please add your galaxy TOKEN first!")
        sys.exit(1)
    else:
        args.func(conn, vars(args))

if __name__=='__main__':
    main()