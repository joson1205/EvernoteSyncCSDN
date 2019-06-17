#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-13 10:19:39
# @Author  : joson (859699677@qq.com)
# @Link    : https://joson1205.github.io/
# @Version : $Id$

import configparser

# 调用读取配置模块中的类
conf = configparser.ConfigParser()
conf.read("config.ini", encoding="utf-8-sig")

Evernote_username = conf.get("Evernote_Setting", "username")
Evernote_password = conf.get("Evernote_Setting", "password")
CSDN_username = conf.get("CSDN_Setting", "username")
CSDN_password = conf.get("CSDN_Setting", "password")

CSDN_status = conf.get("CSDN_Setting", "status")
CSDN_article_type = conf.get("CSDN_Setting", "article_type")
CSDN_categories = conf.get("CSDN_Setting", "categories")
CSDN_channel = conf.get("CSDN_Setting", "channel")
CSDN_private = conf.get("CSDN_Setting", "private")


if __name__ == '__main__':
    print(CSDN_article_type)
