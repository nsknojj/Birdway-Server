# -*- coding: utf-8 -*-
import os
import json
import Users
from Users import connect


def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not ('authorization',) in tables:
        cursor.execute('CREATE TABLE authorization ('
                       'id  INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'filename    TEXT    NOT NULL, '
                       'username    TEXT    NOT NULL,'
                       'auth    INTEGER);')
        conn.commit()
    cursor.close()
    conn.close()
    return


def have_edit_auth(filename, username):
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' AND username='" + username + "';"
    cursor.execute(s)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(ret) == 0:
        return 0
    return ret[0][0] >= 1


def have_manage_auth(filename, username):
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' AND username='" + username + "';"
    cursor.execute(s)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(ret) == 0:
        return 0
    return ret[0][0] >= 2


def get_edit_list(username):
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT filename FROM authorization WHERE username='" + username + "';"
    cursor.execute(s)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    return ret


def change(filename, username, auth, myname):
    if auth == -1:
        for user in Users.all_users():
            if user[0] != myname:
                change(filename, user[0], 1, myname)
        return

    if auth == -2:
        for user in Users.all_users():
            if user[0] != myname:
                change(filename, user[0], 0, myname)
        return

    conn = connect()
    cursor = conn.cursor()
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' AND username='" + username + "';"
    # print s
    cursor.execute(s)
    ret = cursor.fetchall()
    if len(ret) == 0:
        s = "INSERT INTO authorization (filename, username, auth) " + \
            "values ('" + filename + "', '" + username + "', " + str(auth) + ");"
        cursor.execute(s)
        conn.commit()
    else:
        s = "UPDATE authorization SET auth=" + str(auth) + \
            " WHERE filename='" + filename + "' AND username='" + username + "';"
        # print s
        cursor.execute(s)
        conn.commit()


create_table()
# print Users.all_users()
change('a.txt', 'zwt', -2, 'zwt')
# change('a.txt', 'zwt', 2, 'zwt')
