#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
交互tty前置操作,将列表中的数据进行处理
"""
import os, sys, prettytable

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from modules.db_fetch import *
import modules.jump_server


def jump():
    """
    遍历用户查询的信息列表,显示序列号,主机名,IP地址
    :param user: 当前登录用户
    :return:
    """
    while True:
        # 获取但当前登录用户
        user = os.getlogin()
        #打印相关用户能操作的服务器信息
        row = prettytable.PrettyTable()
        row.field_names = ['序列号', '主机名', 'IP地址']
        #调用fetch函数,得到服务器列表信息,以及log日志所需要的userprofile_id
        ret,userprofile_id = fetch(user)
        #pretty列表打印列表信息
        for item in ret:
            row.add_row([ret.index(item), item[0][0], item[0][1]])
        print(row)
        #用户选择序列号
        inp = input('请输入需要操作的服务器对应的序号,输入\033[31;1mexit退出\033[0m:')
        if inp == 'exit':
            print('交互tty操作退出!')
            break
        else:
            try:
                inp = int(inp)
            except:
                print('选择有误,请重新选择!')
            else:
                #选择正确后,从列表中取到服务器登录的信息
                if inp < len(ret):
                    info = ret[inp]
                    ip = info[0][1]
                    port = info[0][2]
                    username = info[1][2]
                    pwd = info[1][3]
                    hostuser_id = info[1][4]
                    # print(userprofile_id,hostuser_id)
                    # print(ip,port,username,pwd)
                    try:
                        #调用paramiko的tty交互登录目标服务器
                        modules.jump_server.run(ip,port,username,pwd,userprofile_id,hostuser_id)
                    except:
                        print('登录信息有误,请联系管理员更新服务器信息')
                else:
                    print('选择有误,请重新选择')
