#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#

""" ak相关 """

import db

def get_info(ak):
    return db.mysql.get(
        "SELECT * FROM `ak` WHERE `ak` = %s", ak)
