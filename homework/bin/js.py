#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

"""
主程序入口
"""
import os, sys, prettytable

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import modules.jump_run
import modules.batch_op
import modules.batch_upload


def logout():
    exit('程序退出')

def show():
    """
    主菜单函数
    :return:
    """
    row = prettytable.PrettyTable()
    row.field_names = ['交互式shell操作','批量服务器命令行操作','批量上传文件至服务器','退出']
    row.add_row([0,1,2,'3&q'])
    print(row)

menu_list = [modules.jump_run.jump,modules.batch_op.batch,modules.batch_upload.upload,logout]
def js_run():
    while True:
        show()
        inp = input('请选择对应操作功能的序列号,q退出程序!')
        if inp == 'q':
            logout()
        else:
            try:
                inp = int(inp)
            except:
                print('选择输入有误,请重新选择!')
            else:
                if inp < len(menu_list):
                    menu_list[inp]()
                else:
                    print('选择有误!请重新输入')

if __name__ == '__main__':
    js_run()