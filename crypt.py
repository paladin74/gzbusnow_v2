#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-12-16
#

""" 加解密 """

import base64
import urllib
import constants

from Crypto.Cipher import DES

try:
    import ujson as json
except ImportError:
    import json

class DESCipher():
    """ DES加解密 """

    def __init__(self, key):
        self.bs = DES.block_size
        self.iv = constants.CRYPT_IV
        self.key = key

    def encrypt(self, params):
        raw_data = self._pad(urllib.urlencode(params))
        cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
        enc_data = base64.b64encode(cipher.encrypt(raw_data))
        return enc_data

    def decrypt(self, enc_str):
        enc_data = base64.b64decode(enc_str)
        cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
        dec_data = cipher.decrypt(enc_data)
        return json.loads(self._unpad(dec_data))

    def _pad(self, s):
        pad_len = self.bs - len(s) % self.bs
        return s + pad_len * chr(pad_len)

    def _unpad(self, s):
        return s[:-ord(s[-1])]

cipher = DESCipher(constants.SITE_MOBILE[1])
