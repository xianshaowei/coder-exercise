# -*- coding:utf8 -*-

from dailycoder.conf import CONF

if __name__ == "__main__":

    for i in CONF.enabled_apis:
        print("DEFAULT.enabled_apis: " + i)

    for i in CONF.apis_opt:
        print("DEFAULT.apis_opt: " + i)