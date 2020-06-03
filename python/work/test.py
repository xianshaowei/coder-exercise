# -*- coding: utf-8 -*-

import json
import requests

from oslo_config import cfg


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

    # return (finish_run, stdoutput.strip(), erroutput.strip())
    return (finish_run, stdoutput.strip().strip("\'"), erroutput.strip())


def config_load(repo):
    print("repo is %s" % repo)
    reponame = cfg.OptGroup(name=repo, title='group repo Options')
    opts = [
        cfg.StrOpt('project', default='', help='the  project  of in config group .'),
        cfg.StrOpt('yamlfile', default='', help='the  yamlfile  of in config group .'),
        cfg.StrOpt('jsonfile', default='', help='the  jsonfile  of in config group, only luna start process need .'),
        cfg.StrOpt('start_method', default='', help='the  project  of in config group .')
    ]

    # 注册选项
    cfg.CONF.register_group(reponame)
    cfg.CONF.register_opts(opts, group=reponame)

    # 指定配置文件
    cfg.CONF(default_config_files=['repo.conf'])

    resu = 'cfg.CONF' + '.monitor_adapter.project'
    print(resu)
    print(cfg.CONF.monitor_adapter.project)
    # print(cfg.CONF.reponame.project)
    # print(cfg.CONF.monitor_adapter.project)
    # print(cfg.CONF.monitor_adapter.yamlfile)
    # print(cfg.CONF.monitor_adapter.jsonfile)
    # print(cfg.CONF.monitor_adapter.start_method)


def fileread():
    import json
    with open('filetest.txt', 'rb') as fp:
        fp_result = fp.read()
        adict = json.loads(fp_result)
        print(type(adict))



def main():
    #config_load('monitor_adapter')
    #fileread()

    # 将字典写入文件
    json_info = {'age': '12', 'a': 2}
    file = open('ttt.txt', 'wb')
    json.dump(json_info, file)

    # 将字符串转换为字典
    bstr = '{ "a" : 1, "b" : 2 }'
    bdict = json.loads(bstr)
    print(bdict)




if __name__ == '__main__':
    main()
