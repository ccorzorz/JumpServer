#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
日志处理模块
"""
import os, sys, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from modules.db_fetch import *

def write_log(userprofile_id,hostuser_id,cmd):
    """
    将操作日志写入数据库函数
    :param userprofile_id: 登录用户的ID
    :param hostuser_id: 当前操作用户的ID
    :param cmd: 操作命令
    :return:
    """
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ss.add(Log(userprofile_id=userprofile_id,hostuser_id=hostuser_id,date=date,cmd=cmd))
    ss.commit()
