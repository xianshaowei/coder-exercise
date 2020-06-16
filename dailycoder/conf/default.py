from oslo_config import cfg
import sys
# 声明配置项模式
# 单个配置项模式
enabled_apis_opt = cfg.ListOpt('enabled_apis',
                                default=['ec2', 'osapi_compute'],
                                help='List of APIs to enable by default.')
# 注册单个配置项模式
def register_opts(conf):
    conf.register_opt(enabled_apis_opt)

