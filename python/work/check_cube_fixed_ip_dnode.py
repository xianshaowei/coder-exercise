#!/usr/bin/python
# ! -*- encoding:utf-8 -*-


import re
import socket
from oslo_config import cfg
import json
import requests
import time
import os
import gpost


AUTH_URL = "http://auth.nie.netease.com/api/v1"
AUTH_USER = "_cld_readonly"
AUTH_KEY = "56972b6fff3e48b7a0edf4ceae58da17"
AUTH_CACHE_FILE = "/tmp/auth_token"

GALAXY_URL = "https://galaxy.nie.netease.com/api/v1"

cube_conf = "/home/cld/conf/cube/cube.conf"

TOKEN_EXPIRE = 10 * 365 * 60

class Auth(object):
    """auth token creater"""
    def __init__(self, auth_user=AUTH_USER, auth_key=AUTH_KEY, ttl=None):
        self.cache_file = AUTH_CACHE_FILE
        self.auth_user = auth_user
        self.auth_key = auth_key
        if ttl:
            self.ttl = int(ttl)
        else:
            self.ttl = TOKEN_EXPIRE
        self.auth_url = AUTH_URL
        if not os.path.exists(self.cache_file):
            f = open(self.cache_file, "w")
            f.close()

    def create_token(self):
        """
        generate cube token from auth
        :return:
        """
        path = '/tokens'
        url = self.auth_url + path
        # 设置token的有效期，0到8天中的一个随机数
        #ttl = int(random.random() * (60 * 60 * 24 * 8))
        data = {
            'user': self.auth_user,
            'key': self.auth_key,
            'ttl': self.ttl,
        }
        try:
            result = requests.post(url=url, json=data)
        except Exception as e:
            return None
        if not str(result.status_code).startswith("20"):
            res = None
        else:
            try:
                res = result.json()
                # 将key从token信息中删除,保证只传送token和expire和user，不传送key保证安全性
                res.pop('key')
            except ValueError as e:
                res = None
        return res

    def _get_cached_token(self):
        token_info_s = read_file(self.cache_file)
        return token_info_s

    def _write_cache_token(self, content):
        write_file(self.cache_file, content)

    def get_token_from_cache(self):
        """get_token_from cache"""
        token_info_s = self._get_cached_token()
        for record in token_info_s:
            try:
                jrecord = json.loads(record.strip())
            except ValueError:
                continue
            user = jrecord["user"]
            expire = jrecord["expire"]
            token = jrecord["token"]
            NOW_TIMESTAMP = int(time.time())
            if user == self.auth_user and (not expire or int(expire) - NOW_TIMESTAMP >= 20):
                # 找到一个没有过期的对应user的token记录，直接返回退出本方法
                # 下面的语句将不再执行
                return token
            elif user == self.auth_user and expire - NOW_TIMESTAMP < 20:
                # 找到一个已经过期的对应user的token记录，在记录中删除
                token_info_s.remove(record)
        # 如果跑到这里了，说明找不到可用的 token 了
        return None

    def cache_token(self, new_token_info):
        """
        缓存token，判断是否已经有同一个user的token，有的话要删掉，最后把新增的token信息缓存进去
        :param new_token_info:
        :return:
        """
        # 将新创建的token信息添加到token_info_s列表中，并写到cache中
        # 避免第一次写入空行，需要先判断一下是否为空
        token_info_s = self._get_cached_token()
        token_list = []
        # 把缓存中的信息转换为元素为字典的列表
        for record in token_info_s:
            try:
                jrecord = json.loads(record.strip())
            # 忽略不是缓存格式的行
            except ValueError:
                continue
            user = jrecord["user"]
            expire = jrecord["expire"]
            token = jrecord["token"]
            # 如果缓存中的 user 和新的 token 信息的 user 不一样，那么添加到 list 里面
            # 换言之如果一样那么就丢弃了，反正后面需要把新的 token 信息添加进来
            if user != new_token_info["user"]:
                token_list.append(
                    {
                        "user": user,
                        "expire": expire,
                        "token": token
                    }
                )
        # 将新的 token 信息加进到 token_list， 重新组成需要缓存的内容
        token_list.append(new_token_info)
        # 将 token_list 里面的字典元素 dumps 成 string，存到 token_string_list
        token_string_list = []
        for record in token_list:
            token_string_list.append(json.dumps(record))
        # 将 token_string_list join 成字符创，然后缓存
        token_string = '\n'.join(token_string_list)
        self._write_cache_token(token_string)


    def get_token(self, writecache=True, readcache=True):
        """
        get the token，search the cache file first，create from auth if failed
        """
        # 通过 readcache 参数表示是否从 cache 中获取 token，True or False
        if readcache:
            # 从 cache 中获取 token， 如果不为None，那么直接返回 token
            token = self.get_token_from_cache()
            if token:
                return token
        # 如果语句执行到这里，说明没有找到可用的token信息，那么就创建一个
        new_token_info = self.create_token()
        # 如果在创建token的时候有异常，那么返回None
        if not new_token_info:
            return None
        # 是否写入缓存
        if writecache:
            self.cache_token(new_token_info)
        # 一切正常的时候返回 token
        return new_token_info["token"]

    def get_user(self):
        return self.auth_user

def read_file(cfile):
    f = open(cfile, "r")
    res = f.readlines()
    f.close()
    return res

def write_file(cfile, content_list):
    f = open(cfile, "w")
    for i in content_list:
        f.write(i)
    f.close()


class GalaxyApi(object):
    def __init__(self, authentication):
        self.galaxy_url = GALAXY_URL
        self.auth_token = authentication["auth_token"]
        self.auth_user = authentication["auth_user"]
        self.auth_project = self.auth_user.split("_")[1]
        self.headers = {
            'X-Auth-Token': self.auth_token,
            'X-Auth-Project': self.auth_project,
        }

    def get_machine_by_ip(self, ip):
        path = "/machines?_ip=%s" % ip
        url = GALAXY_URL + path
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            result = resp.json()
            if int(result['total']) == 1:
                return result["items"][0]
            else:
                return None
        else:
            return None




def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def _get_default_fixed_ips_host():
    # 定义参数
    galaxy_opts = [
        cfg.StrOpt(
            "default_fixed_ips_host",
            help="default fixed ips host in galaxy"),
        cfg.StrOpt(
            "default_resource_type",
            help="cluster type, vm or cntr"
        )
    ]

    CONF.register_opts(galaxy_opts)
    _ip = CONF.default_fixed_ips_host
    if not isIP(_ip):
        _ip = socket.gethostbyname(_ip)
    return _ip

def get_cluster_type():
    cluster_opts = [
        cfg.StrOpt(
            "default_resource_type",
            help="cluster type, vm or cntr"
        )
    ]
    CONF.register_opts(cluster_opts)
    _cluster_type = CONF.default_resource_type
    return _cluster_type


def alert(msg):
    '''
    定义报警的方法，并且定义报警的data字典里面type=cube_fixip_dnode
    :param list:
    :return:
    '''
    alter_data = {
        "type": "cube_fixed_ip_dnode",
        "status": 1,
    }
    gpost.blackhole(data=alter_data, msg=msg)

def main():
    global CONF
    CONF = cfg.CONF
    CONF(default_config_files=['/home/cld/conf/cube/cube.conf'])

    cluster_type = get_cluster_type()
    # 只在容器集群执行
    if cluster_type == "cntr":
        _ip = _get_default_fixed_ips_host()

        _auth = Auth()
        auth_token = _auth.get_token()
        auth_project = _auth.get_user()
        authentication = {
            "auth_token": auth_token,
            "auth_user": auth_project
        }
        galaxy = GalaxyApi(authentication)
        # 判断一下是否可以从 galaxy 中找到机器
        # 如果返回 None，那么是没有，就报警
        if not galaxy.get_machine_by_ip(_ip):
            msg = "galaxy 中不存在 ip 为 %s 的机器，请检查 cube 的配置项 default_fixed_ips_host。" % _ip
            alert(msg)
    else:
        pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        msg = "检查 cube 配置的脚本出现 Exception：%s (脚本位置 %s)" % (e.message, os.path.abspath(__file__))
        alert(msg)