#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#

"""辅助类

"""

import yaml
import os.path
import hashlib
import logging
import os
import socket
import struct
import db
import ujson as json

class YamlLoader(yaml.Loader):
    """ Yaml loader

    Add some extra command to yaml.

    !include:
        see http://stackoverflow.com/questions/528281/how-can-i-include-an-yaml-file-inside-another
        include another yaml file into current yaml
    """

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YamlLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)

YamlLoader.add_constructor('!include', YamlLoader.include)


class Loggers(object):
    """简单的logging wrapper"""

    def __init__(self):
        self.loggers = {}

    def use(self, log_name, log_path):
        if not log_name in self.loggers:
            logger = logging.getLogger(log_name)
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                fh = logging.FileHandler(log_path)
                fh.setLevel(logging.INFO)
                formatter = logging.Formatter('%(asctime)s - %(message)s')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
            self.loggers[log_name] = logger
        return self.loggers[log_name]

loggers = Loggers()


def db_cache(master_key, ttl=86400):
    """ 数据库缓存 """
    def db_cache_wrap(method):
        def wrapper(slave_key, *args, **kwargs):
            key_name = "apiv2:%s:%s" % (master_key, slave_key)
            data = db.redis.get(key_name)
            if not data:
                data = method(slave_key, *args, **kwargs)
                if data:
                    db.redis.setex(key_name, json.dumps(data), ttl)
            else:
                data = json.loads(data)
            return data
        return wrapper
    return db_cache_wrap


def md5(raw_str):
    return hashlib.new("md5", str(raw_str)).hexdigest()


def sha1(raw_str):
    return hashlib.new("sha1", str(raw_str)).hexdigest()


def ip2int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])


def int2ip(int_ip):
    return socket.inet_ntoa(struct.pack("I", socket.htonl(int_ip)))
