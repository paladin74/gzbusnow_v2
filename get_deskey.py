#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rsa
import requests
import base64
from pyDes import *

def main():
    pubkey, prikey = rsa.newkeys(1024)
    p = bytearray.fromhex('00'+hex(pubkey.n)[2:-1]+'010001')
    p = base64.b64encode(p)
    url1 = 'http://g3.gzyyjt.net:7007/unicom/data'
    url2 = 'http://info-3g.gzyyjt.net:8008/unicom/data'
    url3 = 'http://info.gzyyjt.net:9009/unicom/data'
    # mobile MOKFV700
    # tianyi B4AHQK2G
    # unicom XTEIZDDM
    for url in [url1, url2, url3]:
        r = requests.post(url, data=p)
        print rsa.decrypt(base64.b64decode(r.text), prikey)

def main2():
    data1 = 'W3XlRl93M9fKkqKNYyfUT50fvyWM2RT4kK39kUupMBDVevWZxlRQFFt2j0xE YZajkX/aDybeqKTYzc5KBLm/FYx39tAKBSnwPw2+AfpNslyk74/mZNm1lBuA vg/OAp+w3n7CghprayM='
    data2 = 'a1qox+YyQmw93wq8lI2MI4Lj1SkAjyyivPR3qZ7lMB1mqVMQbc06VPC7+Rxs ZPeYJQppWzmPyuSaZ6bnCxGNWNthZ186mqQq4l5cztbCElP+sbV4GAVezDmi +vaVMzUXnWY03IL6HW2xAboJS8whOtsxHUWbzHIa5BCxQOLVxD3nSvS3AAN4 8cQWHQFM/MRW'
    data3 = 'W3XlRl93M9dbhl4aWRDfQ6+DFFKQd0730xoUkSZCvDmxtv4KghqVzmCqCAd+ YEBrHvqAL2HEHVja/ga1veysmoVdJ8Ytd+pOXCpBG59DXqPHMPzEQxcn7wac gt/eiNiAXNPmb1UpdHmB/OK8x/U87NYBXwSccWVkezL2NnGUAnU1qMgCLXMm BhHRY897CXBMbxfHjt52XwZ8j1Yl84ZiGr0I937fGmr+W66yHXdZExycG2Jg g8BFj+VTQVGyrR1g78NwpEqQtNxcA2KuAVfuMGxPYECdpQeo'
    data4 = 'cC5HdSwSBQDGYDKUiE1u9EVJwFSKb+cH4n+HHP8X4EOGG6wH+IyykSNtfiYg K0ow3CRyy+XqftassakITxI1xSHE1Kq1qtrxOq6+0naRj43uFEH6wXSn5M4X 2LeYdTYxzc/5AD1tzgnBd9iImRnTBKyPZLJw2jmAjfkJYMCwaPZ+4H5SEY5I yLHawrJyJjw42bY/3AP1rMfbFHWLNsE4pS49tIT9fgn2CHXGIldEOPFehq6P orz3WvBINUme0hcMwiw+nEXyAtM='
    for data in [data1, data2, data3, data4]:
        enc = base64.b64decode(data)
        descipher = des("B4AHQK2G", CBC, b'\x01\x09\x08\x02\x00\x07\x00\x05', pad=None, padmode=PAD_PKCS5)
        print descipher.decrypt(enc)


if __name__ == "__main__":
    main2()
