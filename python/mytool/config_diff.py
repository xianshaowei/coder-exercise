# -*- coding: utf-8 -*-
"""
-------------------------------------------------

   Description :
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019
-------------------------------------------------
   Change Activity:
                   2019
-------------------------------------------------

此脚本适用于比较key=value格式的配置文件
使用方式为：
config_diff.py old_file new_file
最终会将new_file中的新增配置项添加入old_file中，old_file中已有的配置项不会做任何改变。

"""


import re
import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")



def conf_to_dict(file):
    ''' 将config文件转换为dict'''
    import re
    import os, sys
    key_vaule_list = []
    group_list = []
    file_dict = {}
    with open(file,'r') as f:
        for oneline in f:
            #print line.strip()
            line = oneline.strip()

            if re.match('^#', line) or re.match('^$', line):
                continue

            if line in file_dict.keys():
                print("config value is error:")
                print(line)
                sys.exit()

            if re.match('^\[.*\]$', line):
                group_tag = line.strip()
                file_dict[group_tag] = {}
                #print file_dict
                continue
            else:
                line_split = line.strip().split('=', 1)
                if len(line_split) == 2:
                    k, v = line_split
                    file_dict[group_tag][k] = v
                else:
                    print("config value is error:")
                    print(line)
                    sys.exit()
    return file_dict



def main():
    try:
        file01 = sys.argv[1]
        file02 = sys.argv[2]
    except Exception, e:
        print("Error:" + str(e))
        print("Usage: config_diff.py file01 file02")
        sys.exit()


    # for k,v in conf_to_dict(file01).iteritems():
    #     print( "%s : %s" %(k,v))

    dict01 = conf_to_dict(file01)
    dict02 = conf_to_dict(file02)

    if cmp(dict01,dict02) == 0:
        print("OK,config file %s and %s are the same." %(file01,file02))
    else:
        print("Error,config file %s and %s are different.pls use vimdiff to check." %(file01,file02))
        sys.exit()

if __name__ == "__main__":
    main()