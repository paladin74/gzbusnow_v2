#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#
""" 主要逻辑 """

import torndb
import tornado.web
import server
import redis
import db
import constants
import protocols

from service import gzbus, phone, ipregion

class Application(server.Application):

    def startup(self):
        """处理各种数据库链接等

        比如:
            self.db = torndb.Connection(
                host=self.config.mysql_host,
                database=self.config.mysql_database,
                user=self.config.mysql_user,
                password=self.config.mysql_password)
        """
        self.db = db.mysql = torndb.Connection(**self.config['mysql'])
        pool = redis.ConnectionPool(
            host=self.config['redis']['host'],
            port=self.config['redis']['port'])
        self.redis = db.redis = redis.Redis(connection_pool=pool)

        # ip库初始化
        ipregion.IPInit()


class MainHandler(protocols.JSONBaseHandler):

    def get(self):
        self.write("hello world!")


if __name__ == '__main__':
    handlers = [
        (r"/", MainHandler),
        (r'/static/(.*)',
            tornado.web.StaticFileHandler,
            {'path': constants.STATIC_DIR}),

        # 公交查询
        (r"/bus", gzbus.GZBusnowHandler),
        # 手机查询
        (r"/phone", phone.PhoneRegionHandler),
        # IP查询
        (r"/ip", ipregion.IPRegionHandler),
    ]

    server.mainloop(Application(handlers))
