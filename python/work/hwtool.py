#!/usr/bin/env python
#coding: utf8
"""
Author: hjt - hjtn1266@corp.netease.com
Created date: 2016-10-24 16:57
Last modified: 2019-08-29 18:10
Filename: hwtool.py
Description:
    merge the hwtool info.
"""

import os
import sys
import signal
from optparse import OptionParser


LOG_LEVEL = 'info'

VALID_ACTION_LIST = ['info']
#VALID_ACTION_LIST = ['info']
VALID_MODULE_LIST = []

class MyParser(OptionParser):
    '''MyParser 模块'''
    def print_usage(self, file=None):
        '''redefine usage'''
        if self.usage:
            print >>file, self.get_usage()
            print >>file, '''Support Mail:
  matrix.sa@list.nie.netease.com\n'''

    def format_help(self, formatter=None):
        '''redefine help'''
        if formatter is None:
            formatter = self.formatter
        result = []
        if self.usage:
            result.append(self.get_usage() + "\n")
        if self.description:
            result.append(self.format_description(formatter) + "\n")
        result.append(self.format_option_help(formatter))
        result.append(self.format_epilog(formatter))
        result.append('''\nUsage:''')
        result.append('''\n  Actions:
      %s''' % (', '.join(VALID_ACTION_LIST)))
        result.append('''\n  Modules:
      all, %s''' % (', '.join(VALID_MODULE_LIST)))
        result.append('''\n  Led on/off example:
      hwtool -l ctrl=<ctrlnum> pd="<slotnum1>,<slotnum2>" on/off''')
        result.append('''\n  Create RAID example:
      hwtool -r <raid_level> ctrl=<ctrlnum> pd="<slotnum1>,<slotnum2>"''')
        result.append('''\n  Set JBOD Mode example:
      hwtool -j ctrl=<ctrlnum> pd="<slotnum1>,<slotnum2>"\n''')
        result.append('''\nSupport Mail:
  matrix.sa@list.nie.netease.com\n''')
        return "".join(result)

    def error(self, msg):
        '''redefine error'''
        self.exit(2, "%s\n" % msg)

    def print_error(self, msg, err_code):
        '''redefine print_error function'''
        self.exit(err_code, "%s\n" % msg)

    def _add_version_option(self):
        '''redefine _add_version_option'''
        self.add_option("-v", "--version",
                        action="version",
                        help="show the version and exit")

def args_parse():
    '''parsing arguments'''
    usage = "%prog [Options]"
    ver_str = "%%prog: %s" % VERSION
    parser = MyParser(usage, version=ver_str)
    parser.add_option("-a", "--action", \
                        metavar="ACTION", \
                        dest="action", \
                        help="use ACTION function of hwtool")
    parser.add_option("-m", "--module", \
                        metavar="MODULE", \
                        dest="module", \
                        help="use module MODULE")
    parser.add_option("-f", "--fms", \
                        action="store_true", \
                        dest="hardware", \
                        help="display fms infomation")
    parser.add_option("-H", "--history", \
                        action="store_true", \
                        dest="history", \
                        help="display fms infomation")
    parser.add_option("-t", "--synctime", \
                        dest="synctime", \
                        action="store_true", \
                        help="use hwtool set hardware time")
    parser.add_option("-d", "--detail", \
                        dest="detail", \
                        action="store_true", \
                        help="display detail hardware infomation")
    parser.add_option("-e", "--extend-args", \
                        metavar="EXTEND_ARGS", \
                        dest="extend_args", \
                        help="extend arguments for some action")
    parser.add_option("-l", "--led", \
                        metavar="on|off", \
                        dest="led", \
                        action="store_true", \
                      help="turning on/off disk led location indicators")
    parser.add_option("-j", "--jbod", \
                        metavar="JBODCREATE", \
                        dest="jbodadd", \
                        action="store_true", \
                        help="use hwtool set disk jbod mode")
    parser.add_option("-r", "--raid", \
                        metavar="RAID_LEVEL", \
                        dest="raidadd", \
                        help="use hwtool create raid volumes")

    # default: using hwtool info function to show hw infomation
    if (len(sys.argv) < 2):
        return  ("info", VALID_MODULE_LIST, "", False)

    (opts, args) = parser.parse_args(sys.argv[1:])
    #print args

    if opts.detail:
        detail_status = True
    else:
        detail_status = False

    if args:
        '''old args support'''
        # print opts.led
        if opts.led:
            action = "led"
            module_list = []
            extend_args = args
            detail_status = opts.led

        elif opts.raidadd:
            action = "raidadd"
            module_list = []
            extend_args = args
            detail_status = opts.raidadd

        elif opts.jbodadd:
            action = "jbod"
            module_list = []
            extend_args = args
            detail_status = "jbod"

        else:
            if not args[0] in VALID_ACTION_LIST:
                parser.print_help()
                sys.exit(0)
            action = args[0]

            if len(args) == 1:
                module_list = VALID_MODULE_LIST
                extend_args = []
            else:
                module_list = args[1:2]
                extend_args = args[2:]
                if module_list[0] not in VALID_MODULE_LIST:
                    print "Invalid module name: %s" % (module_list[0])
                    sys.exit(1)
    else:
        '''new args format in version 3.0'''
        if (opts.action is None):
            if not (opts.raidadd or \
                    opts.led or \
                    opts.jbodadd or \
                    opts.raidadd):
                action = "info"
            else:
                print "create raid args incomplete."
                sys.exit(1)
        else:
            action = opts.action
        if (not action in VALID_ACTION_LIST):
            err_msg = "Invalid action name: %s" % (action)
            parser.print_error(err_msg, err_code=3)

        if opts.hardware:
            module_list = ['hardware']
            detail_status = True
        elif opts.history:
            module_list = []
            detail_status = True
            from hardware import diff_format
            diff_format()
        elif opts.synctime:
            #module_list = ['synctime']
            module_list = []
            detail_status = True
            from clock import CLOCK
            CLOCK().set_hwclock()
        else:
            if (opts.module is None) or (opts.module == "all"):
                module_list = VALID_MODULE_LIST
            else:
                module_list = opts.module.split(',')
                for m in module_list:
                    if (not m in VALID_MODULE_LIST):
                        err_msg = "Invalid module name: %s" % (m)
                        parser.print_error(err_msg, err_code=4)

        if (not opts.extend_args is None):
            extend_args = opts.extend_args.split(',')
        else:
            extend_args = []

    # print (action, module_list, extend_args, detail_status)
    return (action, module_list, extend_args, detail_status)


def print_format_info(module_list=VALID_MODULE_LIST, \
        exclude=False, \
        detail_info=False):
    """ use MODULE.format method to print all info """
    from product import PRODUCT
    from cpu import CPU
    from memory import MEMORY
    from gpu import GPU
    from network import NETWORK
    from bond import BOND
    from disk import DISK
    from raid import RAID
    #from sel import SEL
    from fan import FAN
    from power import POWER
    # from clock import CLOCK
    from hardware import HARDWARE

    infokey = {'product': PRODUCT,
               'cpu': CPU,
               'memory': MEMORY,
               'gpu': GPU,
               'network': NETWORK,
               'bond': BOND,
               'disk': DISK,
               'raid': RAID,
               'fan': FAN,
               'power': POWER,
               'hardware': HARDWARE,
              }

    # print module_list, VALID_MODULE_LIST
    if exclude:
        modules = set(VALID_MODULE_LIST) - set(module_list)
    else:
        modules = set(module_list)

    #module_list = ('product', 'cpu', 'memory', 'network', 'fan', 'disk')
    for module in module_list:
        if module in modules:
            output_string = 'Loading %s INFO...' % module
            print '%-30s' %output_string,
            sys.stdout.write("\r")
            sys.stdout.flush()

            myinfo = infokey[module]()
            print '%-50s' %'',
            sys.stdout.write("\r")
            sys.stdout.flush()
            if detail_info == False:
                myinfo.brief_format()
            else:
                myinfo.format()

    return


def print_info(info, extend_info={}, level=0):
    '''print info pretty'''
    mytype = type(info)

    #print 'Info: %s' %info
    #print 'Ext:  %s' %extend_info


    if (mytype == type('str')) or (mytype == type(1)):
        extend_info.setdefault('unit', '')
        print info, extend_info['unit']
    elif (mytype == type((1,))) or (mytype == type([])):
        if not info:
            print
            return
        if (type(info[0]) == type('str')) or (type(info[0]) == type(1)):
            extend_info.setdefault('unit', '')
            print info, extend_info['unit']
            return

        for i in info:
            print_info(i, level+1)

    elif mytype == type({}):
        if level > 0:
            print
        index = 0
        for key in info:
            if level == 0 and index > 0:
                print
            print '%s%s:' % ('    ' * level, extend_info[key]['name']),
            print_info(info[key], extend_info[key], level+1)
            index += 1
    else:
        print info
    return


def sigint_handler(signum, frame):
    '''handle ctrl+c signal'''
    print "\nEXIT: user interrupted."
    sys.exit(9)


if __name__ == '__main__':
    # capture ctrl+c signal
    signal.signal(signal.SIGINT, sigint_handler)

    if os.path.islink(__file__):
        link_path = os.readlink(__file__)
    else:
        link_path = __file__
    FILE_PATH = os.path.abspath(os.path.dirname(link_path))
    PATH = os.path.abspath(FILE_PATH+'/../module/')
    sys.path.insert(0, PATH)

    from common import VALID_MODULE_LIST, VERSION
    from common import HWTOOL, get_info
    #from func import run


    hwtool = HWTOOL()
    hwtool.loadmod()
    log = hwtool.LOG('HWTOOL', level=LOG_LEVEL).log

    (action, module_list, extend_args, detail_status) = args_parse()
    log('Action: %s' % action)
    log('Module: %s' % module_list)
    log('Extend: %s' % extend_args)
    log('Detail: %s' % detail_status)

    if action == "info":
        if len(module_list) == 1 and len(extend_args) > 0:
            if len(extend_args) <= 1:
                try:
                    (info, extend_info) = get_info(module_list=module_list, \
                    extend_args=extend_args)
                except:
                    print 'Get module information failed.'
                else:
                    print_info(info, extend_info)
            else:
                print 'Too many extend arguments.'
        else:
            print_format_info(module_list=module_list, \
                exclude=False, \
                detail_info=detail_status)

    elif action == "synctime":
        pass

    elif action == "led" or \
            action == "raidadd" or \
            action == "jbod":
        from raidctrl import RAIDCTRL
        pd_action = detail_status
        ctrl_num = 0
        isled = 0
        for e_args in extend_args:
            e_args_list = e_args.split("=")
            if len(e_args_list) == 2:
                if e_args_list[0] == "ctrl":
                    #print e_args_list
                    ctrl_num = int(e_args_list[1])
                elif e_args_list[0] == "pd":
                    pd_slot_str = str(e_args_list[1])
                    #pd_slot_str = str(e_args_list[1]).strip('[]')
                    pd_slot_raw = pd_slot_str.split(",")
                    pd_slot_list = []
                    for pd_slot in pd_slot_raw:
                        if str(pd_slot).find('-') != -1:
                            pd_slot_split = str(pd_slot).split('-')
                            if len(pd_slot_split) != 2:
                                print "have some args error: %s" % pd_slot
                                sys.exit(1)
                            else:
                                try:
                                    pd_slot_start = int(pd_slot_split[0])
                                    pd_slot_stop = int(pd_slot_split[1]) + 1
                                except:
                                    print "have some args error: %s" % pd_slot
                                    sys.exit(1)
                                for pd_slot_one in range(pd_slot_start, pd_slot_stop):
                                    pd_slot_list.append(pd_slot_one)
                        elif pd_slot.isdigit():
                            pd_slot_list.append(int(pd_slot))
                        else:
                            print "have some args error: %s" % pd_slot
                            sys.exit(1)

            if action == "led":
               if e_args == "on" or \
                       e_args == "off":
                   isled = 1
                   pd_action = e_args

        #if pd_slot_list is None:
        if 'pd_slot_list' not in dir():
            print 'pd slot args error'
            sys.exit(1)

        raidct = RAIDCTRL(ctrl_num)
        if action == "led":

            if isled != 1:
                print 'led operation no args: on/off'
                sys.exit(1)
            raidct.pdlocate(pd_action, pd_slot_list)
        elif action == "raidadd" or \
                action == "jbod":
            raidct.raidcreate(pd_action, pd_slot_list)