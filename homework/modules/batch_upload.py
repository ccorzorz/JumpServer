#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
批量上传模块核心
"""
import os, sys, prettytable, time, paramiko

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from modules.db_fetch import *
from modules.logger import *


def help():
    print('''
使用方法:
1. 操作服务器对象:输入操作服务器正确的序列号,多台服务器使用逗号隔开
2. 操作命令:与操作服务器对象隔开,输入命令
3. 注意:如果操作服务器对象中,如果有错误选择,批量操作无法执行
4. \033[31;1m正确例子:1,2,4 localpath/filename remopath/filename\033[0m
    ''')


def upload():
    while True:
        # 获取但当前登录用户
        user = os.getlogin()
        # 打印相关用户能操作的服务器信息
        row = prettytable.PrettyTable()
        row.field_names = ['序列号', '主机名', 'IP地址']
        # 调用fetch函数,得到服务器列表信息,以及log日志所需要的userprofile_id
        ret, userprofile_id = fetch(user)
        # print(ret)
        # pretty列表打印列表信息
        for item in ret:
            row.add_row([ret.index(item), item[0][0], item[0][1]])
        print('可操作的服务器'.center(40, '*'))
        print(row)
        # 用户选择序列号
        inp = input('序列号1,序列号2,序列号3 command(输入\033[31;1mexit退出,h帮助\033[0m):')
        if inp == 'exit':
            print('批量操作程序退出!')
            break
        elif inp == 'h':
            help()

        else:
            # 用户输入拆分为
            inp_list = inp.split(' ')
            host_id_list = inp_list[0].split(',')
            cmd = ' '.join(inp_list[1:])
            try:
                id_list = []
                for i in host_id_list:
                    id_list.append(int(i))
            except:
                print('序列号输入有误!')
                help()
                time.sleep(1)
            else:
                try:
                    info_list = []
                    for i in id_list:
                        info_list.append(ret[i])
                except:
                    print('服务器对应序列号选择有误!')
                    help()
                    time.sleep(1)
                else:
                    upload_op(info_list, cmd, userprofile_id)
                    print('执行完成')


def upload_op(info_list, cmd, userprofile_id):
    for item in info_list:
        # 取值,赋予登录信息变量值
        hostname = item[0][0]
        ip = item[0][1]
        port = item[0][2]
        username = item[1][2]
        passwd = item[1][3]
        hostuser_id = item[1][4]
        try:
            localpath,remopath = cmd.split(' ')
        except:
            print('本地文件以及远程文件路径定义有误!')
            help()
            time.sleep(1)
        else:
            # 实例化对象
            obj = Sftp(ip, port, username, passwd, hostname)
            obj.run(localpath,remopath)
            # 写入日志
            write_log(userprofile_id, hostuser_id, cmd)


class Sftp:
    def __init__(self, ip, port, username, passwd, hostname):
        """
        构造方法,初始化ssh
        :param ip: IP地址
        :param port: 端口
        :param username:用户名
        :param passwd: 密码
        :param hostname: 服务器的hostname
        :return:
        """
        self.transport = paramiko.Transport((ip, port))
        self.transport.connect(username=username, password=passwd)
        self.stfp = paramiko.SFTPClient.from_transport(self.transport)
        self.hostname = hostname

    def run(self, localpath, remopath):
        """
        执行上传命令函数
        :param localpath: 本地文件路径以及文件名
        :param remopath: 目的服务器中的路径以及文件名
        :return:
        """
        try:
            self.stfp.put(localpath, remopath)
        except Exception as ex:
            print('%s:上传出错!' % self.hostname)
            print(ex)
            help()
            time.sleep(1)
        else:
            print('%s:上传完成!' % self.hostname)


# if __name__ == '__main__':
#     upload()