# -*- coding: utf-8 -*-
import mysql.connector
import sqlite3


def connect():
    return sqlite3.connect('MyServer.db')
    # return mysql.connector.connect(user='root', password='', database='MyServerDB')


def insert_user(name, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not ('user',) in tables:
        cursor.execute('CREATE TABLE user ('
                       'id  INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'name    TEXT    NOT NULL, '
                       'password    CHAR(100));')
        conn.commit()

    s = "SELECT name FROM user WHERE name='" + name + "';"
    cursor.execute(s)
    name_list = cursor.fetchall()
    if len(name_list) > 0:
        return 0

    s = "INSERT INTO user (name, password) " + "values ('" + name + "', '" + password + "');"
    # print s
    cursor.execute(s)
    conn.commit()
    print 'Insert user, name: ', name
    cursor.close()
    conn.close()
    return 1


def get_user(name='admin', id=0):
    conn = connect()
    cursor = conn.cursor()
    ret = []
    if id > 0:
        cursor.execute("SELECT * FROM user WHERE id=" + str(id))
        ret = cursor.fetchall()
    elif name != 'admin':
        cursor.execute("SELECT * FROM user WHERE name='" + name + "'")
        ret = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(ret) > 0:
        print 'Get user', ret[0]
        return ret[0]
    else:
        print 'No such user'
        return []


# please make sure the user exists
def get_password(name='admin', id=0):
    return get_user(name=name, id=id)[2]


def all_users():
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT name FROM user;"
    cursor.execute(s)
    return cursor.fetchall()


# print insert_user(name='ab', password='1213')
