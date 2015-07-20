#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import requests
import urllib
import time
import sys
import json

from pyDes import *

reload(sys)
sys.setdefaultencoding('utf-8')

descipher = des("B4AHQK2G", CBC, b'\x01\x09\x08\x02\x00\x07\x00\x05', pad=None, padmode=PAD_PKCS5)
url = 'http://info-3g.gzyyjt.net:8008/unicom'

def main():
    data1 = 'W3XlRl93M9cz9SSDmucCKblqhjcC7T1kKS2fmfCyMEx3+s3IywryPjjMuXoT cg30e/03H0hSBW1gLNml9U5PPe3h8nkME5cZ/2Mh5ZNJBjEk8IlIAyTXM4Yb VmNhzmuV7BSLj7PzWA0='
    data2 = 'cC5HdSwSBQDGYDKUiE1u9EVJwFSKb+cH4n+HHP8X4EOGG6wH+IyykSNtfiYg K0ow3CRyy+XqftassakITxI1xSHE1Kq1qtrxOq6+0naRj43uFEH6wXSn5M4X 2LeYdTYxzc/5AD1tzgnBd9iImRnTBKyPZLJw2jmAjfkJYMCwaPZ+4H5SEY5I yLHawrJyJjw42bY/3AP1rMfbFHWLNsE4pS49tIT9fgn2CHXGIldEOPFehq6P orz3WvBINUme0hcMwiw+nEXyAtM='
    data3 = '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 um7CTw=='
    data4 = 'cC5HdSwSBQDGYDKUiE1u9EVJwFSKb+cH4n+HHP8X4EOGG6wH+IyykSNtfiYg K0ow3CRyy+XqftassakITxI1xSHE1Kq1qtrxOq6+0naRj43uFEH6wXSn5M4X 2LeYdTYxzc/5AD1tzgnBd9iImRnTBKyPZLJw2jmA89tsZzBrWIbm0Dd3CNnn mMrm7we4d78cM1qmkjTKmvnBV8tlzgOKeGxBUsIuy/53iyaKfkuZSpAjlNTg O3AG0KGCWpXlnVMP+3e1vRv32Udr9rOLBD/RwQ=='
    data5 = 'cC5HdSwSBQDGYDKUiE1u9EVJwFSKb+cH4n+HHP8X4EOGG6wH+IyykSNtfiYg K0ow3CRyy+XqftassakITxI1xSHE1Kq1qtrxOq6+0naRj43uFEH6wXSn5M4X 2LeYdTYxzc/5AD1tzgnBd9iImRnTBKyPZLJw2jmAjfkJYMCwaPZ+4H5SEY5I yLHawrJyJjw42bY/3AP1rMfbFHWLNsE4pS49tIT9fgn2CHXGIldEOPFehq6P orz3WvBINUme0hcMEYDvmZ+HMco='
    data6 = 'W3XlRl93M9cz9SSDmucCKcvC4nJTvkCKA1Gxm6056Nrjbel2FiJcXcEwg5Ji zkF+brBk8Xcgxr8uzT3eKg8NMavkNFDW1YFb/+QRRBVOj2bNuyUV/UGUGlyX SBEnPIMTmoYWXN4r3XOLN8AsRsXvvCEp/QvuKciAGe4aEJzelSDZr4Fneohk /lqjDP8WfAAK1qrsihOsU3fcf0zEFuCWoiUgdx6rQqwSW0pj+W0+t10U/4Zt PEdcwssuhd47wMd9qmiEVR75ru7puRMovUztsJDO9pACuQIw4U0fnd7aQP1G sOf60lQxq/d3tadZuHAoT6Pg7vwqGw1zY+AuHmDqPBe8nAoE0RF7skiPcA2H 1Udgcw+fluBqFq4wffcguazZgRLu2BsfsdZ2kyjVn29COcm5DZHcFHh+YJkR edT6Kdw2eSYAEgg6BAlWrDpdzXo7Sxa0Usw/FutRLCBxBd0WUN3f/8JVulN1 TUgsa3c8Bwq/c1roda5f+Jp2zTlLu9BB+qAeVl8RyebGwDbDqs5XxM5gAvSZ Kk6HJ1u1/1MRYE5HVYCGr5LJX/o2BbvO5pKr56jykkwW07I='
    datas = [data1, data2, data3, data4, data5, data6]
    i = 1
    for data in datas:
        enc = base64.b64decode(data)
        descipher = des("B4AHQK2G", CBC, b'\x01\x09\x08\x02\x00\x07\x00\x05', pad=None, padmode=PAD_PKCS5)
        print i, descipher.decrypt(enc)
        i += 1

def get_bus(oper, route):
    params = {
        "username": "android",
        "password": "123456",
        "IMSI": "460000290762763",
        "devNumber": "0000000029F6B0C400000000454D8D02VIXPZQKPIK",
        "version": "2.5.8",
        "devType": 0,

        "type": "line",
        "queryType": 1,
        "oper": oper, # detail or fuzzy
        "routeName": route.encode('gbk'),
    }

    raw_data = urllib.urlencode(params)
    enc_data = base64.b64encode(descipher.encrypt(raw_data))
    start = time.time()
    r = requests.post(url+'/Bus', data=enc_data)
    if r.status_code == 200:
        dec_data = descipher.decrypt(base64.b64decode(r.text))
        data = json.loads(dec_data)
        print data['content']
    else:
        print "server error!"

    print time.time()-start


if __name__ == "__main__":
    get_bus('detail', '大学城2线')
