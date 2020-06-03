#!/usr/bin/env bash
# !/usr/bin/env python
# this script is used for allocate available ip for hangzhou develop vm

import sys
import netaddr
import subprocess
import shlex
import logging
from netaddr import *
from subprocess import PIPE
from logging.handlers import WatchedFileHandler
import glob
import requests
import os
import json

HEAD_SKIP = 11
TAIL_SKIP = 10

VMLIST = "/home/vm/cephfs/etc/vmlist.*"
HOST_IP_POOL_MAP = {
    "HZ_NET_I": "10.246.13.0/24",
    "HZ_NET_II": "10.246.14.0/24",
    "HZ_NET_III": "10.246.17.0/24"
}
VM_IP_POOL_MAP = {
    "HZ_NET_I": "10.246.44.0/23",
    "HZ_NET_II": "10.246.46.0/23",
    "HZ_NET_III": "10.246.52.0/23"
}

LOGFILE = "/home/vm/var/log/allocate_ip.log"
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)
HANDLER1 = logging.StreamHandler(sys.stdout)
# WatchedFileHandler is a kind of filehandler
HANDLER2 = WatchedFileHandler(LOGFILE)
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s", \
                          "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setFormatter(FMTER)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_valid_cidr(address):
    """Verify that address represents a valid CIDR address.
    :param address: Value to verify
    :type address: string
    :returns: bool
    """
    try:
        # Validate the correct CIDR Address
        netaddr.IPNetwork(address)
    except (TypeError, netaddr.AddrFormatError):
        return False

    # Prior validation partially verify /xx part
    # Verify it here
    ip_segment = address.split('/')
    if len(ip_segment) <= 1 or ip_segment[1] == '':
        return False
    return True


def is_address_in_network(network, address):
    """
    Determine whether the provided address is within a network range.

    :param network: (str) CIDR presentation format. For example,
        '192.168.1.0/24'.
    :param address: An individual IPv4 or IPv6 address without a net
        mask or subnet prefix. For example, '192.168.1.1'.
    :returns boolean: Flag indicating whether address is in network.
    """
    try:
        network = netaddr.IPNetwork(network)
    except (netaddr.AddrFormatError, ValueError):
        raise ValueError(
            "Network (%s) is not in CIDR presentation format" % network)
    try:
        address = netaddr.IPAddress(address)
    except (netaddr.AddrFormatError, ValueError):
        raise ValueError(
            "Address (%s) is not in correct presentation format" % address)
    if address in network:
        return True
    else:
        return False


def run_cmd(cmd):
    """run bash cmd"""
    LOG.debug("run cmd: %s" % cmd)
    args = shlex.split(cmd)
    for i in args:
        if "*" in i:
            head_items = args[:args.index(i)]
            tail_items = args[args.index(i) + 1:]
            args = head_items + glob.glob(i) + tail_items
    fp = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = fp.communicate()
    if fp.returncode != 0:
        e = Exception("cmd: %s error. %s" % (cmd, str(err)))
        LOG.exception(e)
        sys.exit(fp.returncode)
    else:
        # LOG.debug(str(out).strip())
        return str(out).strip()


def get_my_ip():
    """get local host ip address"""
    out = run_cmd("hostname -i")
    LOG.debug("get myip: %s" % out)
    return str(out)


def get_used_iplist():
    """get used ip list"""
    out = run_cmd("""cat %s""" % VMLIST)
    used_iplist = []
    for line in out.split('\n'):
        if not line.startswith("#") and len(line.split()) > 2:
            used_iplist.append(line.split()[2])
    return used_iplist


def get_token():
    '''read TOKEN from file "TOKEN" if exist'''
    token_path = os.path.dirname(os.path.abspath(__file__))
    token = token_path + "/TOKEN"
    if os.path.isfile(token):
        TOKEN = open(token).read().strip()
        return TOKEN
    else:
        return ""


def is_exist_galaxy(ip):
    url = "https://galaxy.nie.netease.com/api/v1/bll/machines/spotlight"
    _headers = {
        'X-AUTH-PROJECT': 'cld',
        'X-AUTH-TOKEN': get_token(),
        'Content-Type': 'application/json'
    }
    params = {"name": ip}
    r = requests.get(url, params=params, headers=_headers, verify=False)
    if r.status_code in [200, 201, 204, 206]:
        try:
            result = json.loads(r.text)
            if len(result) > 0:
                LOG.error(
                    "in galaxy and hostname:%s project:%s" % (result[0]['name'], result[0]['project']['projectName']))
                return True
            return result
        except ValueError:
            return None
    LOG.error("access url failed! status:%s" % r.status_code)
    return None


def check_ping(ip):
    """check ip ping ok or failed"""
    cmd = "ping -W1 -c3 %s" % ip
    args = shlex.split(cmd)
    fp = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = fp.communicate()
    # print out
    return fp.returncode


def allocate_ip(host_ip, num=1):
    """allocate unused ip according host ip"""
    host_net = None
    count = 1
    ac_ips = []
    for name, cidr in HOST_IP_POOL_MAP.iteritems():
        if is_address_in_network(cidr, host_ip):
            host_net = name
            break
    if not host_net:
        LOG.error("can't find host_ip:%s belong host_cidr: %s"
                  % (host_ip, HOST_IP_POOL_MAP))
        sys.exit(1)
    vm_pool_cidr = VM_IP_POOL_MAP.get(host_net)
    if not vm_pool_cidr:
        LOG.error("can't find host_ip:%s allocate ip pool cidr: %s"
                  % (host_ip, VM_IP_POOL_MAP))
        sys.exit(1)
    used_ips = get_used_iplist()
    used_ips.sort()
    # for i in used_ips:
    #    print i
    # print str(vm_pool_cidr).split("/")[1]
    if int(vm_pool_cidr.split("/")[1]) > 24:
        LOG.error("vm pool cidr netmask large than 24!")
        sys.exit(1)
    vm_c_cidr = IPNetwork(vm_pool_cidr)

    for ip in vm_c_cidr[HEAD_SKIP:-TAIL_SKIP]:
        ##add select from galaxy
        if str(ip) in used_ips:
            pass
            # if str(ip) in used_ips:
            #   alc = "true"
            # else:
            #    alc = "false"
            # LOG.debug("pass %s\t%s" % (ip,alc))
        elif is_exist_galaxy(str(ip)):
            LOG.warn("ip:%s is existed in galaxy,SKIP....." % str(ip))
            continue
        else:
            LOG.info("preallocate " + bcolors.WARNING + "%s" % ip
                     + bcolors.ENDC)
            LOG.info("check ping ...")
            if check_ping(str(ip)) == 0:
                LOG.error(bcolors.FAIL +
                          "%s is pingable! skip it, allocate again"
                          % ip + bcolors.ENDC)
            else:
                LOG.info("comfirm allocate " + bcolors.OKGREEN + "%s" % ip
                         + bcolors.ENDC)
                ac_ips.append(str(ip))

                if count < num:
                    count = count + 1
                    continue

                if len(ac_ips) > 1:
                    LOG.info("comfirm allocate ips:" + bcolors.OKGREEN + " %s" % ','.join(ac_ips) + bcolors.ENDC)

                return ac_ips


def show_ip():
    used_ips = get_used_iplist()
    # print used_ips
    for k, ip_pool in VM_IP_POOL_MAP.iteritems():
        ips = IPNetwork(ip_pool)
        for index, ip in enumerate(ips):
            if str(ip) in used_ips:
                state = 'Allocated'
            elif index < HEAD_SKIP or index > len(ips) - TAIL_SKIP:
                state = 'Reserved'
            else:
                state = 'Unallocated'

            print
            '%s\t%s' % (ip, state)


def main():
    myip = get_my_ip()
    todo = ""

    try:
        if sys.argv[1] == 'show':
            todo = 'show'
        else:
            num = int(sys.argv[1])

    except (IndexError, ValueError):
        num = 1

    if todo == 'show':
        show_ip()
    else:
        allocate_ip(myip, num)


if __name__ == "__main__":
    main()