#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
交互式TTY操作模块核心程序
"""
import os, sys, paramiko, socket, getpass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from modules.db_fetch import *
from modules.logger import *
# python3版本不需要注释,版本2需要注释掉
from paramiko.py3compat import u

# windows does not have termios...
#使用异常判断系统是否有tty,定义has_termios变量
try:
    import termios
    import tty

    has_termios = True
except ImportError:
    has_termios = False

#定义进入交互TTY的函数
def interactive_shell(chan, userprofile_id, hostuser_id):
    if has_termios:
        posix_shell(chan, userprofile_id, hostuser_id)
    else:
        windows_shell(chan)


def posix_shell(chan, userprofile_id, hostuser_id):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        #设置超时时间
        chan.settimeout(0.0)
        # f = open('handle.log', 'a+')
        tab_flag = False
        # cmd_temp_list = []
        while True:
            #socket模块,监听socket的变化
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if tab_flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            # cmd_temp_list.append(x)
                            # f.write(x)
                            # f.flush()
                            # if len(cmd_temp_list) == 20:
                            #     cmd_str=''.join(cmd_temp_list)
                            write_log(userprofile_id, hostuser_id, x)
                        tab_flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                if x == '\t':
                    tab_flag = True
                else:
                    # cmd_temp_list.append(x)
                    # f.write(x)
                    # f.flush()
                    # if len(cmd_temp_list) == 20:
                    #     cmd_str=''.join(cmd_temp_list)
                    #操作写入日志数据库
                    write_log(userprofile_id, hostuser_id, x)
                chan.send(x)
    #最后恢复tty原来的默认值,否则会影响以后的登录操作
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass


def run(ip, port, username, pwd, userprofile_id, hostuser_id):
    #使用transport模块,传入参数
    tran = paramiko.Transport((ip, port,))
    tran.start_client()
    tran.auth_password(username, pwd)
    # 打开一个通道
    chan = tran.open_session()
    # 获取一个终端
    chan.get_pty()
    # 激活器
    chan.invoke_shell()
    #传入参数,调用进入TTY交互操作
    interactive_shell(chan, userprofile_id, hostuser_id)

    chan.close()
    tran.close()


