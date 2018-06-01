#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import pkgutil
sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.utils.hashutil import HashUtil

def print_password():
    if len(sys.argv) > 1:
        print HashUtil().sha1(sys.argv[1])
    else:
        print "Usage: ", sys.argv[0], " <password>"
if __name__ == '__main__':
    print_password()
