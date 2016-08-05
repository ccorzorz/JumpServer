#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
通过用户查询数据库,将有操作权限的服务器信息列表化并返回
"""
import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from db.db_strut import *

def fetch(login_user):
    """
    通过用户查询有操作权限的服务器信息,将数据形成列表
    :param login_user: 登录用户帐号
    :return:
    """
    #通过第三张关系表(虚拟关系hostid_list)查询user_profile中登录用户对应的登录用户信息,并形成有序列表
    ret = ss.query(UserProfile).filter(UserProfile.username==login_user).first()
    userprofile_id = ret.id
    user_info=[]
    for item in ret.hostid_list:
        user_info.append((item.host_id,item.auth_type,item.username,item.password,item.id))
    #遍历用户信息的表,查询到host表中的id对应的hostname,ip以及端口好,并形成有序列表
    login_info=[]
    for item in user_info:
        ret = ss.query(Host).filter(Host.id==item[0]).first()
        login_info.append((ret.hostname,ret.ip_addr,ret.port))
    #zip两个列表,由于是有序列表,所以信息是互相对应的
    result_list=list(zip(login_info,user_info))
    # print(result_list)
    return result_list,userprofile_id
