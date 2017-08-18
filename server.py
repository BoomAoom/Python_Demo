#!/usr/bin/env python
# -*-coding:utf-8-*-

import socket
import hashlib
import os
import select


def my_exexists(username):
    path1 = os.path.dirname(__file__)
    path2 = os.path.join(path1, 'home', username)
    ret = os.path.exists(path2)
    return ret


def my_hashlib(passwd):
    has = hashlib.md5(bytes('z8z8', encoding='utf-8'))
    has.update(bytes(passwd, encoding='utf-8'))
    has_passwd = has.hexdigest()
    return has_passwd


def login(username, passwd):
    ret = my_exexists(username)
    if ret:
        path2 = os.path.join(os.path.dirname(__file__), 'home', username)
        f = open(path2, "rb")
        if my_hashlib(passwd) == str(f.read(), encoding="utf-8"):
            return '102'  # 登入成功
        else:
            return '101'  # 密码错误
    else:
        return '100'  # 账号不存在


def register(username, passwd):
    ret = my_exexists(username)
    if not ret:
        path1 = os.path.dirname(__file__)
        path2 = os.path.join(path1, 'home', username)
        f = open(path2, "wb")
        ret = my_hashlib(passwd)
        f.write(bytes(ret, encoding='utf-8'))
        f.close()
        return True
    else:
        return False


def my_server():
    ser = socket.socket()
    ser.bind(("127.0.0.1", 8001))
    ser.listen()
    inputs = [ser, ]
    while True:
        r, w, e = select.select(inputs, [], [], 1)
        for ser_or_conn in r:
            if ser_or_conn == ser:
                conn, adder = ser.accept()
                conn.sendall(bytes("----hello----", encoding='utf-8'))
                inputs.append(conn)
            else:
                try:
                    chosse = conn.recv(1024)
                except Exception as EX:
                    inputs.remove(ser_or_conn)
                else:
                    if str(chosse, encoding='utf-8') == "2":
                        try:
                            creation_user = conn.recv(1024)
                            username, passwd = str(creation_user, encoding="utf-8").split('/')
                        except Exception as EX:
                            inputs.remove(ser_or_conn)
                        else:
                            result = register(username, passwd)
                            if result:
                                conn.sendall(bytes('Register complete！', encoding='utf-8'))
                            else:
                                conn.sendall(bytes('Username Already Exists Or No None!', encoding="utf-8"))
                                inputs.remove(ser_or_conn)
                    elif str(chosse, encoding='utf-8') == "1":
                        try:
                            login_user = conn.recv(1024)
                            username, passwd = str(login_user, encoding="utf-8").split('/')
                            result = login(username, passwd)
                        except Exception as EX:
                            inputs.remove(ser_or_conn)
                        else:
                            if result == "100":
                                conn.sendall(bytes("100", encoding='utf-8'))
                            elif result == "101":
                                conn.sendall(bytes("101", encoding='utf-8'))
                            elif result == "102":
                                conn.sendall(bytes("102", encoding='utf-8'))


if __name__ == '__main__':
    my_server()
