# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 
   Description :   用协程实现批量下载文件
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019
-------------------------------------------------
   Change Activity:
                   2019
-------------------------------------------------
"""

import sys
import urllib
import time
reload(sys)
sys.setdefaultencoding("utf-8")

import gevent
from gevent import monkey
monkey.patch_all()

def downloadfile(url):
    filename_to_list = url.split("/")
    filename = filename_to_list[-1]
    try:
        print("%s 开始下载......" % filename)
        ret = urllib.urlopen(url)  # ret = urllib.request.urlopen(url)   #python3.7
        with open(filename, "wb") as fb:
            while True:
                data = ret.read(1024)
                if data:
                    fb.write(data)
                else:
                    break
        print("%s 下载完成\n" % filename)
    except Exception  as e:
        print(e)
        print("%s 下载失败！！！\n" % filename)


def main():
    url4 = "http://cld-admin1:8080/hardware/vnode/dell/ixgbevf-4.5.3.tar.gz"
    url3 = "https://www.cdfangxie.com/Public/uploadfile/file/2019/06/14/20190614184652_25618.pdf"
    url2 = "http://cld-admin1:8080/unix_sed_awk.pdf"
    url1 = "https://www.cdfangxie.com/Public/uploadfile/file/2019/06/17/20190617171828_60533.pdf"

    # 非协程
    # downloadfile(url2)
    # downloadfile(url3)
    # downloadfile(url4)  # 0.54

    # 协程方法一
    # g2 = gevent.spawn(downloadfile, url2)
    # g3 = gevent.spawn(downloadfile, url3)
    # g4 = gevent.spawn(downloadfile, url4)
    #
    #
    # g2.join()
    # g3.join()
    # g4.join() # 0.59

    #协程方法二
    gevent.joinall([
        gevent.spawn(downloadfile, url1),
        gevent.spawn(downloadfile, url2),
        gevent.spawn(downloadfile, url3),
        gevent.spawn(downloadfile, url4)
    ])



if __name__ == '__main__':

    time_start = time.time()
    main()
    print time.time() - time_start
