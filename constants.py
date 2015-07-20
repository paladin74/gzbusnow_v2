#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#

import os.path


""" Tornado Server 定义 """
# 接收到关闭信号后多少秒后才真正重启
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
# Listen IPV4 only
IPV4_ONLY = True


""" 全局配置常量 """
CRYPT_IV = '\x01\x09\x08\x02\x00\x07\x00\x05'
SITE_MOBILE = ("http://g3.gzyyjt.net:7007/unicom/", "MOKFV700")
SITE_TELECOM = ("http://info-3g.gzyyjt.net:8008/unicom/", "B4AHQK2G")
SITE_UNICOM = ("http://info.gzyyjt.net:9009/unicom/", "XTEIZDDM")

BASEURL = "http://apiv2.chenjiehua.me"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

""" 协议、校验错误 """
ERR_PROTOCOL_ERROR = (-1001, "协议解析错误")
ERR_INTERNAL_ERROR = (-1002, "内部错误")
ERR_INVALID_AK = (-1003, "ak无效")
ERR_INVALID_TIMESTAMP = (-1004, "时间戳无效")

""" 公交相关 """
ERR_OPER_ERROR = (-2001, "参数oper错误")
ERR_SERVER_BUSY = (-2002, "服务器繁忙，请稍微重试")
ERR_NOT_FOUND = (-2003, "查询无结果！")
ERR_DIRECTION_ERROR = (-2004, "方向参数错误")
ERR_ENCODE_ERROR = (-2005, "编码错误")
