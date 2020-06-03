# -*- coding: utf-8 -*-

import sys
from oslo_config import cfg
from oslo_config import types

# 自定义端口类型，范围在(1, 65535)
PortType = types.Integer(1, 65535)

opts = [
    cfg.StrOpt('ip',
               default='127.0.0.1',
               help='IP address to listen on.'),
    cfg.Opt('port',
            type=PortType,
            default=8080,
            help='Port number to listen on.')
]

# 注册选项
cfg.CONF.register_opts(opts)

# group database
DATABASE = cfg.OptGroup(name='database',
                        title='group database Options')
opts = [
    cfg.StrOpt('connection',
               default='',
               help='item connection in group database.')
]
cfg.CONF.register_group(DATABASE)
cfg.CONF.register_opts(opts, group=DATABASE)

# 指定配置文件
cfg.CONF(default_config_files=['test.conf'])

print('DEFAULT: ip=%s  port=%s' % (cfg.CONF.ip, cfg.CONF.port))
print('database: connection=%s' % (cfg.CONF.database.connection))
