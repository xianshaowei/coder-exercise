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

import os, sys, re
import logging
from logging.handlers import WatchedFileHandler

sys.setdefaultencoding("utf-8")


def main():
    print(os.environ.get('DEBUG'))


if __name__ == '__main__':
    main()
