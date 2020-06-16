# -*- coding:utf8 -*-
from oslo_config import cfg
import sys
from . import default
from . import api


CONF = cfg.CONF
CONF(sys.argv[1:], default_config_files=['/Users/netease/Documents/git/coder-exercise/dailycoder/conf/my.conf'])
default.register_opts(CONF)
api.register_opts(CONF)