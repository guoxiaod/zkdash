#!/usr/bin/env python2.7

import hashlib, binascii
from conf.settings import AUTH
from lib.utils import logger


class HashUtil(object):
    def __init__(self):
        self._salt = AUTH['salt']

    def sha1(self, password):
        dk = hashlib.pbkdf2_hmac('sha1', password, self._salt, 10000)
        return binascii.hexlify(dk)


    def sha256(self, password):
        dk = hashlib.pbkdf2_hmac('sha256', password, self._salt, 10000)
        return binascii.hexlify(dk)

if __name__ == '__main__':
    pass
