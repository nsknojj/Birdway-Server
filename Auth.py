# -*- coding: utf-8 -*-
import os
import json
import Files
import Users
from Users import connect


def insert_editor(filename, username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not ('authorization',) in tables:
        cursor.execute('CREATE TABLE editor ('
                       'id  INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'filename    TEXT    NOT NULL, '
                       'username    TEXT    NOT NULL,'
                       'auth    INTEGER);')
        conn.commit()

    s = "SELECT name FROM authorization WHERE username='" + username + "' filename='" + filename + "';"
    cursor.execute(s)
    editor_list = cursor.fetchall()
    if len(editor_list) > 0:
        return 0

    s = "INSERT INTO editor (filename, username) " + "values ('" + filename + "', '" + username + "');"
    # print s
    cursor.execute(s)
    conn.commit()
    print 'Insert editor (filename, username): ', filename, username
    cursor.close()
    conn.close()
    return 1


# def query_editor(filename, username):
#     conn = connect()
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()
#     if not ('editor',) in tables:
#         cursor.close()
#         conn.close()
#         return 0
#
#     s = "SELECT name FROM editor WHERE username='" + username + "' filename='" + filename + "';"
#     cursor.execute(s)
#     editor_list = cursor.fetchall()
#     if len(editor_list) > 0:
#         return 1


def have_edit_auth(filename, username):
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' username='" + username + "';"
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
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' username='" + username + "';"
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


def change(filename, username, auth):
    if auth == -1:
        pass
    if auth == -2:
        pass
    conn = connect()
    cursor = conn.cursor()
    s = "SELECT auth FROM authorization WHERE filename='" + filename + "' username='" + username + "';"
    cursor.execute(s)
    ret = cursor.fetchall()
    if len(ret) == 0:
        s = "INSERT INTO authorization (filename, username, auth) " + \
            "values ('" + filename + "', '" + username + "', " + str(auth) + ");"
        cursor.execute(s)
        conn.commit()
    else:
        s = "UPDATE authorization SET auth=" + str(auth) + \
            "WHERE filename='" + filename + "', username='" + username + "';"
        cursor.execute(s)
        conn.commit()
