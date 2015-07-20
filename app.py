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

from service import gzbus

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


class MainHandler(protocols.JSONBaseHandler):

    def get(self):
        self.write("hello world!")


class TestHandler(protocols.JSONBaseHandler):
    """ 测试 """

    def get(self):
        pass


if __name__ == '__main__':
    handlers = [
        (r"/", MainHandler),
        (r"/test", TestHandler),
        (r'/static/(.*)',
            tornado.web.StaticFileHandler,
            {'path': constants.STATIC_DIR}),

        # 公交查询
        (r"/bus", gzbus.GZBusnowHandler),
    ]

    server.mainloop(Application(handlers))
