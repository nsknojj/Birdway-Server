# -*- coding: utf-8 -*-
import os
import json
import threading
path = ''
file_list = dict()
editing = dict()
lock = dict()


def save_file(filename):
    # print 'Save file', filename
    up_file(filename, file_to_string(file_list[filename]))


def add_editor(filename, sock):
    lock[filename].acquire()
    if not (filename in editing):
        editing[filename] = [sock]
    else:
        editing[filename].append(sock)
    lock[filename].release()


def del_editor(filename, sock):
    editing[filename].remove(sock)
    # if len(editing[filename]) == 0:
    #     save_file(filename)
    #     file_list[filename] = []


def string_to_file(s):
    return s.split('\n')


def file_to_string(f):
    ret = ''
    for line in f:
        ret += line + '\n'
    return ret[:-1]


def change(f, modify):
    osx = modify["oldRange"]["start"]["row"]
    osy = modify["oldRange"]["start"]["column"]
    oex = modify["oldRange"]["end"]["row"]
    oey = modify["oldRange"]["end"]["column"]
    osx = min(osx, len(f) - 1)
    oex = min(oex, len(f) - 1)
    osy = min(len(f[osx]), osy)
    oey = min(len(f[oex]), oey)
    if osx == oex:
        tmp = f[osx][:osy] + f[osx][oey:]
        f[osx] = tmp
    else:
        f[osx] = f[osx][:osy] + f[oex][oey:]
        for i in range(osx, oex):
            del f[osx + 1]

    ins_list = modify["newText"].split('\n')
    if len(ins_list) == 1:
        tmp = f[osx][:osy] + ins_list[0] + f[osx][osy:]
        f[osx] = tmp
    else:
        f.insert(osx + 1, ins_list[-1] + f[osx][osy + 1:])
        f[osx] = f[osx][:osy] + ins_list[0]
        length = len(ins_list)
        for i in range(length - 2, 0, -1):
            f.insert(osx + 1, ins_list[i])
    # print file
    # return f


def change_file(filename, modify):
    lock[filename].acquire()
    change(file_list[filename], modify)
    lock[filename].release()
    # save_file(fileNo, '\n'.join(file))


# def delete_file(name):
#     if exist(name):
#         if len(editing[name]) == 0:
#             os.remove(path + name)
#             print name, 'removed'
#             del lock[name]
#         else:
#             print name, 'is being edited'
#     else:
#         print 'No such file'


def exist(name):
    return os.path.exists(path + name)


def down_file(name):
    ret = ''
    if exist(name):
        with open(path + name, 'r') as fin:
            print 'Get file', name
            f = fin.readlines()
            for tmp in f:
                ret += tmp
    else:
        print 'No such file'
    return ret, string_to_file(ret)


# if want to create an empty file, let content = ''
# upload
def up_file(name, content=''):
    lock[name].acquire()
    with open(path + name, 'w') as fout:
        fout.write(content)
        # print 'Upload', name
    lock[name].release()


# def create_file(filename):
#     if exist(filename):
#         return 1
#     with open(path + filename, 'w') as fout:
#         pass
#     print 'Create', filename
#     lock[filename] = threading.Lock()
#     return 0


# return (content, r, c)
def edit_file(filename):
    if filename in file_list:
        line_list = file_list[filename]
        if len(line_list) > 0:
            return file_to_string(line_list)
    ret, file_list[filename] = down_file(filename)
    return ret


# with open(path + 'socketlog2.txt') as modin:
#     file = downFile('a.txt')
#     for mod in modin.readlines():
#         # print type(mod)
#         modify = json.loads(mod.strip())
#         # print type(modify)
#         # print modify
#         change(file, modify)
print ''
