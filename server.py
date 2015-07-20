#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: jiehua233@gmail.com
# @date: 2014-10-24
#
""" 服务器封装，处理各服务器初始化、重启等 """

import tornado.ioloop
import tornado.httpserver
import tornado.web
import yaml
import logging
import signal
import constants
import time
import os

from tornado.options import define, options
from utils import YamlLoader

define("address", default='127.0.0.1', help="绑定指定地址", type=str)
define("port", default=8888, help="绑定指定端口", type=int)
define("debug", default=False, help="是否开启Debug模式", type=bool)
define("autoreload", default=False, help="代码变化的时候是否自动加载代码", type=bool)
define("process", default=-1, help="是否开启都进程模式，默认不开启，0表示跟CPU核数一样", type=int)
define("config", default="settings.yaml", help="配置文件路径", type=str)


class Application(tornado.web.Application):

    def __init__(self, handlers):
        try:
            self.config = yaml.load(file(options.config, 'r'), YamlLoader)
        except yaml.YAMLError as e:
            logging.critical("Error in configuration file: %s", e)

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'template'),
            debug=options.debug,
            autoreload=options.autoreload,
        )

        if 'tornado' in self.config:
            settings.update(self.config['tornado'])

        tornado.web.Application.__init__(self, handlers, **settings)

        self.startup()

    def startup(self):
        """预先初始化某些工作，数据库链接放这里"""
        pass


def mainloop(app):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    if options.process >= 0:
        http_server.bind(options.port, options.address)
        http_server.start(options.process)
    else:
        http_server.listen(options.port, options.address)

    def sig_handler(sig, frame):
        logging.warning('Caught signal: %s', sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    def shutdown():
        logging.info('Stopping http server')
        http_server.stop()  # 不接收新的 HTTP 请求

        logging.info('Will shutdown in %s seconds ...', constants.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + constants.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
                logging.info('Shutdown')
        stop_loop()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    if not options.debug and options.autoreload:
        from tornado import autoreload
        autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
