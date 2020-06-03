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
"""

import os, sys, re, time
import logging
from logging.handlers import WatchedFileHandler
import requests
import json
import urllib3
import argparse
from oslo_config import cfg

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# reload(sys)
# sys.setdefaultencoding("utf-8")

# 定义日志输出

logfile = __file__ + '.log'
LOGFILE = os.path.expanduser(logfile)
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)  # 控制台中输出DEBUG级别的日志
HANDLER1 = logging.StreamHandler(sys.stdout)
HANDLER2 = WatchedFileHandler(LOGFILE)  # WatchedFileHandler is a kind of filehandler
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s ", "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)  # 日志输出格式
HANDLER2.setFormatter(FMTER)  # 日志输出格式
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)


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


def log_test():
    LOG.info("test")
    LOG.error("test2")


def find_diff_item_from_two_list(list01,list02):
    diff_item_num = 0
    for item in list01:
        if item not in list02:
            diff_item_num += 1
            last_item = item
    if diff_item_num == 1:
        return last_item
    else:
        LOG.error('too many diff tag.')
        sys.exit(1)

def file_check(file):
    if os.path.exists(file) == False :
        LOG.error('Error, file %s is not exist.' %file)
        sys.exit(1)

def load_config(file):

    if os.path.exists(file) == False:
        LOG.error('pls check config_file whether exist!')
        sys.exit(1)
    with open(file, 'r') as fp:
        # 读取文件，读取后为结果为一个字符串
        strings = fp.read()
        # 将字符串转换为字典
        mydict = json.loads(strings)
        return mydict


class deal_tag():

    def __init__(self, repo):
        self.token = '35706e37c38ac62177d21bab3264bbb3'
        self.config_dict = load_config('repo.conf')
        self.repo_name = repo
        self.repo_project = self.config_dict[repo]['project']
        self.repo_yamlfile = self.config_dict[repo]['yamlfile']
        self.repo_jsonfile = self.config_dict[repo]['jsonfile']
        self.repo_start_method = self.config_dict[repo]['start_method']
        self.repo_tmpfile = '/tmp/' + repo + '_tag_numbers.txt'



    def get_repo_url(self):

        url = 'https://symphony.nie.netease.com/api/v2/tags?namespace=%s&reponame=%s' % \
                  (self.repo_project, self.repo_name)
        return url

    def get_project_tag(self):
        url = self.get_repo_url()
        _headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        r = requests.get(url, headers=_headers, verify=False)
        LOG.info("get : %s" % url)
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
            return None

    def update_deployment_tag(self, nowtag, newtag):
        yamlfile = self.repo_yamlfile
        change_file_tag = "sed -i 's#%s#%s#' %s" % (nowtag, newtag, yamlfile)
        LOG.info(change_file_tag)
        result = run(change_file_tag)

        LOG.info(run('kubectl get pod --all-namespaces  |grep custom-metrics')[1])

        if result[0] == True:
            apply_yaml_cmd = 'sudo kubectl apply -f %s' % yamlfile
            LOG.info(apply_yaml_cmd)
            apply_result = run(apply_yaml_cmd)
            if apply_result[0]:
                time.sleep(5)
                LOG.info(apply_result[1])
                LOG.info("kube apply sucessfully.")
                LOG.info(run('kubectl get pod --all-namespaces  |grep custom-metrics')[1])
            else:
                LOG.error("kube apply have failed.")
                sys.exit(1)

        else:
            LOG.error("change yaml tags error.")
            sys.exit(1)

        LOG.info(run('kubectl get pod --all-namespaces  |grep custom-metrics')[1])

    def get_current_tag(self):
        if self.repo_start_method == 'yamlfile':
            get_oldtag_cmd = "awk -F '[\:]' /image:/'{print $NF}' %s " % self.repo_yamlfile
            current_tag = run(get_oldtag_cmd)[1]
        elif self.repo_start_method == 'bin':
            pass
        elif self.repo_jsonfile:
            pass

        if current_tag:
            return current_tag
        else:
            return None


def main():


    # 参数处理
    par = argparse.ArgumentParser(description='How to update images for deployment.')
    # 保存参数到namespace
    par.add_argument('--repo', '-r', type=str, help="special a repo")
    # 指定参数
    args = par.parse_args()
    # args.function()
    # print args

    if not args.repo:
        LOG.error('Usage: python update_repo.py -r <xxxxxx>')
        sys.exit(1)

    # 读取配置文件
    config_dict = load_config('repo.conf')
    print(config_dict[args.repo])
    d = deal_tag(args.repo)
    print(d.repo_project)
    print(d.repo_tmpfile)

    if d.repo_start_method == 'yamlfile':
        file_check(d.repo_yamlfile)
    if d.repo_start_method == 'bin':
        file_check(d.repo_jsonfile)

    result = d.get_project_tag()

    if result:
        LOG.info(result)
    else:
        LOG.info("get tags error")
        sys.exit(1)

    new_tags_list = result['tags']
    tag_numbers = len(new_tags_list)

    # 记录当前registry有的tags
    tmpfile = d.repo_tmpfile
    if os.path.exists(tmpfile) == False:
        os.mknod(tmpfile)
        with open(tmpfile, "wb") as fp:
            fp.write(json.dumps(new_tags_list))
        sys.exit(0)
    else:
        with open(tmpfile, "rb") as fp:
            fp_result = fp.read()
            if fp_result:
                old_tags_list = json.loads(fp_result)
            else:
                os.remove(tmpfile)
                sys.exit(1)
        with open(tmpfile, "wb+") as fp:
            fp.write(json.dumps(new_tags_list))



    latest_tags_numbers = len(old_tags_list)
    LOG.info("last_numbers is %s" %latest_tags_numbers)
    LOG.info("tag_numbers of is %s" %tag_numbers)

    # 获取当前tag
    current_tag = d.get_current_tag()

    LOG.info("the tag of running is %s " %current_tag)

    # 判断如果有新tag并满足条件就进行更新
    if latest_tags_numbers != tag_numbers:
        newtag = find_diff_item_from_two_list(new_tags_list,old_tags_list)
        LOG.info("the tag of new image is %s " %newtag)
        if re.match('[0-9]{8}_test_[0-9]{2}', newtag) :
            d.update_deployment_tag(current_tag, newtag)
        else:
            LOG.error("new tag is not correct match,pls push new tag like '20191001_test_01_1124'.")
    else:
        LOG.info("no new tag of image need to update " )


if __name__ == '__main__':
    main()