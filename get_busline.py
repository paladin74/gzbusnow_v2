#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

import torndb
import json
import yaml
import requests

from crypt import cipher
from utils import YamlLoader

SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db = torndb.Connection(**config['mysql'])

def main():
    data = db.get("SELECT * FROM `buskey` WHERE `key` = '.'")
    buses = json.loads(data['line'])
    i = 1
    for bus in buses[455:]:
        print i, bus
        i += 1
        data = get_bus('detail', bus)
        if data['dataType'] in [1]:
            print data['content'], bus
            continue
        for d in data['content']:
            t = d['busLine']
            sd = json.dumps(t)
            db.execute(
                "INSERT INTO `busline`(`lineName`, `firstTime`, `lastTime`, `strPlatName`, `endPlatName`, "
                "`totalPlat`, `lineLength`, `stationNames`, `lineSectCount`, `topFare`, `lineType`, "
                "`lineDirection`, `lineSects`, `corporationInfo`, `flagSubway`, `mapCoords`, `lineId`, "
                "`lineKey`, `ticketPrice`, `interval`, `ticketMode`, `averageTime`, `sourceData`)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                t['lineName'], t['firstTime'], t['lastTime'], t['strPlatName'], t['endPlatName'], t['totalPlat'],
                t['lineLength'], t['stationNames'], t['lineSectCount'], t['topFare'], t['lineType'],
                t['lineDirection'], t['lineSects'], t['corporationInfo'], t['flagSubway'], t['mapCoords'],
                t['lineId'], t['lineKey'], t['ticketPrice'], t['interval'], t['ticketMode'], t['averageTime'], sd
            )


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
    enc_str = cipher.encrypt(params)
    r = requests.post('http://g3.gzyyjt.net:7007/unicom/Bus', data=enc_str)
    if r.status_code == 200:
        dec_data = cipher.decrypt(r.text)
        return dec_data
    else:
        print route

if __name__ == "__main__":
    main()
