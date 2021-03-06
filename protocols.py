#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#

""" JSON交换协议的HTTP Handler """

import tornado.web
import logging
import time
import constants
import ujson as json

from models import aks
from tornado.options import options


class JSONBaseHandler(tornado.web.RequestHandler):
    """ 用于使用JSON做为数据交换格式的基础Handler """

    def write_json(self, response=None):
        """Write json to client"""
        self.set_header('Content-type', 'application/json; charset=UTF-8')
        self.write(json.dumps(response))
        self.finish()

    def write_error(self, status_code, **kwargs):
        """Function to display custom error page defined in the handler.
        Over written from base handler."""

        reason = None
        err = constants.ERR_PROTOCOL_ERROR
        try:
            reason = kwargs['exc_info'][1].reason
            reason = reason if reason is not None \
                else kwargs['exc_info'][1].log_message
        except AttributeError or TypeError:
            err = constants.ERR_INTERNAL_ERROR

        if options.debug:
            logging.warning("Response err: %s" % reason)
            logging.warning("Request: %s" % self.request)

        self.return_error(err, reason)

    def return_success(self):
        self.write_json({"c": 0})

    def return_result(self, result={}):
        self.write_json({"c": 0, "d": result})

    def return_error(self, code, message=None):
        if not message:
            message = code[1]
        self.write_json({"c": code[0], "d": None, "err": {'msg': message}})

    @property
    def config(self):
        return self.application.config

    @property
    def redis(self):
        return self.application.redis

    @property
    def db(self):
        return self.application.db

    def get_ak(self, ak):
        ak_info = aks.get_info(ak)
        return ak_info


class Arguments(object):
    """ 过滤后的参数封装 """

    def __init__(self, arguments):
        self.arguments = arguments

    def get(self, key, default=None, strip=True):
        if key in self.arguments:
            v = self.arguments[key]
            if type(v) is list:
                v = v[0]
            if strip:
                v = v.strip()
            return v
        elif default is not None or "" == default:
            return default
        else:
            raise tornado.web.HTTPError(401, reason=("Argument %s is required" % key))


def ak_required(method):
    """ 请求需配置ak """

    def wrapper(self, *args, **kwargs):
        self.arguments = Arguments(self.request.arguments)
        if self.config['tornado']['debug']:
            return method(self, *args, **kwargs)

        # 判断请求时间
        sec = int(time.time()) - int(self.arguments.get('rt'))
        if sec > 60 or sec < 0:
            return self.return_error(constants.ERR_INVALID_TIMESTAMP)

        # 判断ak
        ak = self.arguments.get('ak')
        self.ak_info = self.get_ak(ak)
        if not self.ak_info or self.ak_info['status'] == 0:
            return self.return_error(constants.ERR_INVALID_AK)

        return method(self, *args, **kwargs)
    return wrapper
