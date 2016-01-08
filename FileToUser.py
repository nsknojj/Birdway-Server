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
    if not ('editor',) in tables:
        cursor.execute('CREATE TABLE editor ('
                       'id  INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'filename    TEXT    NOT NULL, '
                       'username    TEXT    NOT NULL);')
        conn.commit()

    s = "SELECT name FROM editor WHERE username='" + username + "' filename='" + filename + "';"
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


def query_editor(filename, username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not ('editor',) in tables:
        return 0

    s = "SELECT name FROM editor WHERE username='" + username + "' filename='" + filename + "';"
    cursor.execute(s)
    editor_list = cursor.fetchall()
    if len(editor_list) > 0:
        return 1

    return 0
