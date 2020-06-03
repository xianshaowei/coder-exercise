#!/usr/bin/python
# -*- coding: UTF-8 -*-




def is_valid_ip(ip):
    """Returns true if the given string is a well-formed IP address.
    Supports IPv4 and IPv6.
    """
    import socket

    if not ip or '\x00' in ip:
        # getaddrinfo resolves empty strings to localhost, and truncates
        # on zero bytes.
        return False
    try:
        res = socket.getaddrinfo(ip, 0, socket.AF_UNSPEC,
                                 socket.SOCK_STREAM,
                                 0, socket.AI_NUMERICHOST)
        return bool(res)
    except socket.gaierror as e:
        if e.args[0] == socket.EAI_NONAME:
            return False
        raise

def deal_continue_ip_list(ip_string):
    """将形如字符 '1.1.1.1-5' 转换为包括IP地址的 list"""
    # 判断输入IP是否错误，是否错误输入了字母
    iplist = ip_string.split('-')
    #print iplist[0].split('.')
    for i in iplist[0].split('.'):
        try:
            int(i)
        except Exception:
            raise(Exception, "IP number is not a \"int\" type.")
            return False
        if int(i) < 0 or int(i) > 255:
            raise(Exception, "IP number is not in [0,255].")
            #print("Ip list is wrong.")
            #return False
    try:
        int(iplist[-1])
    except Exception:
        raise(Exception, "IP number is not int type.")
    if int(iplist[-1]) < 0 or int(iplist[-1]) > 255:
        raise(Exception, "IP number is not in [0,255].")

    # 切分表达，转换为list
    ip_pre = ".".join(iplist[0].split('.')[0:3]) + "."
    ip_first_suff = iplist[0].split('.')[-1]
    ip_last_suff = iplist[-1]
    res_ip_list = []
    for i in xrange(int(ip_first_suff),int(ip_last_suff)+1):
        if is_valid_ip(ip_pre + str(i)):
            res_ip_list.append(ip_pre + str(i))
    return res_ip_list

def deal_ip_list(ip_string):
    """ 处理形如 10.204.80.11-15,10.204.80.17 ,返回一个ip地址列表list """
    iplist_first_get = ip_string.split(',')
    #print iplist_first_get
    res_ip_list = []
    for i in iplist_first_get:
        if is_valid_ip(i):
            res_ip_list.append(i)
        else:
            for j in deal_continue_ip_list(i):
                res_ip_list.append(j)
    return res_ip_list