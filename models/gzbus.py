#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-12-17
#

""" 公交相关 """

import db
from protocols import db_cache

@db_cache('buskey')
def get_buskey(key):
    return db.mysql.get(
        "SELECT * FROM `buskey` WHERE `key` = %s", key)

def new_buskey(key, line):
    return db.mysql.execute(
        "INSERT INTO `buskey`(`key`, `line`)VALUES(%s, %s)", key, line)

@db_cache('busline')
def get_busline(line):
    return db.mysql.get(
        "SELECT * FROM `busline` WHERE `lineName` = %s LIMIT 1", line)
