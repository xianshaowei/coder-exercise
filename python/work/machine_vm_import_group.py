#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import argparse
import time

project = "cld"
user = "_%s_readonly" % project
sys.path.insert(0, "/home/%s/.virtualenvs/lib/python2.7/site-packages" % project)

from ntessa.resource import GalaxyResource
from ntessa.utils import get_auth_token
from ntessa.error import GalaxyError

BASE_URL = "http://auth.nie.netease.com/api/v1"
# BASE_URL = "http://int.auth.nie.netease.com/api/v1"
auth_key_file = "/home/%s/conf/auth_key.file" % project


def log_message(msg, level='INFO'):
    now = time.time()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    log = '[%s][%s] %s\n' % (time_str, level.upper(), msg)
    sys.stdout.write(log)
    sys.stdout.flush()


def get_auth_key():
    """
    :return: auth_key
    """
    if not os.path.exists(auth_key_file):
        log_message("%s is not exist." % auth_key_file)
        sys.exit(1)
    fp = open(auth_key_file, 'r')
    auth_key = fp.read().strip()
    return auth_key


def get_galaxy_obj(environment):
    """
    """
    auth_key = get_auth_key()
    token = get_auth_token(user, auth_key, ttl=24 * 60 * 60)
    galaxy = GalaxyResource(token, project, debug=environment)
    return galaxy


def checkip_exists_in_galaxy(galaxy, ip):
    """
    Check if IP already exists in galaxy
    """
    machines = galaxy.Machine().filter_by(ip=ip)
    for machine in machines:
        if machine.ip:
            return True

    return False


def import_vm(galaxy, filename):
    log_message("import vm ip from file: %s" % filename)
    bulk = galaxy.Bulk().group_add_machine()

    with open(filename, 'rb') as fp:
        for line in fp:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            l = line.strip().split()
            if len(l) < 5:
                log_message("The number of columns is not enough, please check:%s" % line, 'ERROR')
                continue
            group, role, ip, hostip, vm_type = l

            # Check if IP already exists in galaxy
            ret = checkip_exists_in_galaxy(galaxy, ip)
            if ret:
                log_message("ip: %s already exists in galaxy, skip.... " % line, 'ERROR')
                continue

            _data = {
                "ips": [ip],
                "machineType": vm_type,
                "parent_ip": hostip
            }
            try:
                galaxy.client.post('/machines', _data)
            except GalaxyError as e:
                print e.msg['msg']

            log_message("import vm %s:%s to project %s"
                        % (ip, hostip, project))

            machine = galaxy.Machine().get_one("@%s" % ip)
            service = galaxy.Service().get_one("@%s" % role)
            target_group = galaxy.Group().get_one("@%s" % group)
            bulk.group_add_machine(target_group, machine, [(service, 1)], 1)
        bulk.save()


def arg_parser():
    parser = argparse.ArgumentParser(description='Import virtual machine information to galaxy')
    parser.add_argument('-c', '--config', dest='config', required=True,
                        help='reads the virtual machine configuration file to import.')
    parser.add_argument('-e', '--env', type=str,
                        choices=['test', 'normal'], default='test',
                        help='galaxy environment, eg: test, normal')

    args = parser.parse_args()

    env = {
        'test': {'boolvalue': True, 'label': '测试环境'},
        'normal': {'boolvalue': False, 'label': ' 正式环境'},
    }
    current_env = env.get(args.env, None)
    environment = current_env.get('boolvalue', True)
    filename = args.config

    return filename, environment


def main():
    filename, environment = arg_parser()
    galaxy = get_galaxy_obj(environment)
    import_vm(galaxy, filename)


if __name__ == '__main__':
    main()