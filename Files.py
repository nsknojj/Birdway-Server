# -*- coding: utf-8 -*-
import os
import json
path = 'log/'




def get_file(fileNo):
    return down_file('a.txt')


def save_file(fileNo, content):
    up_file('a.txt', content)


def change(file, modify):
    osx = modify["oldRange"]["start"]["row"]
    osy = modify["oldRange"]["start"]["column"]
    oex = modify["oldRange"]["end"]["row"]
    oey = modify["oldRange"]["end"]["column"]
    if osx == oex:
        tmp = file[osx][:osy] + file[osx][oey:]
        file[osx] = tmp
    else:
        file[osx] = file[osx][:osy] + file[oex][oey:]
        for i in range(osx, oex):
            del file[osx + 1]

    insList = modify["newText"].split('\n')
    if len(insList) == 1:
        tmp = file[osx][:osy] + insList[0] + file[osx][oey:]
        file[osx] = tmp
    else:
        file.insert(osx + 1, insList[-1] + file[osx][osy + 1:])
        file[osx] = file[osx][:osy] + insList[0]
        length = len(insList)
        for i in range(length - 2, 0, -1):
            file.insert(osx + 1, insList[i])
    # print file
    return file


def change_file(fileNo, modify):
    file = get_file(fileNo)
    file = change(file, modify)
    save_file(fileNo, '\n'.join(file))


def delete_file(name):
    if os.path.exists(path + name):
        os.remove(path + name)
        print name, 'removed'
    else:
        print 'No such file'


def exist(name):
    return os.path.exists(path + name)


def down_file(name):
    ret = []
    if exist(name):
        with open(path + name, 'rb') as fin:
            print 'Get file', name
            file = fin.readlines()
            for tmp in file:
                ret.append(tmp.strip())
            if file[-1][-1] == '\n':
                ret.append('')
    else:
        print 'No such file'
    return ret


# if want to create an empty file, let content = ''
def up_file(name='', content=''):
    with open(path + name, 'wb') as fout:
        fout.write(content)
        print 'Save', name


def create_file(filename):
    if exist(filename):
        return 1
    with open(path + filename, 'wb') as fout:
        pass
    print 'Create', filename
    return 0


# return (content, r, c)
def get_file_string(filename):
    pass


# with open(path + 'socketlog2.txt') as modin:
#     file = downFile('a.txt')
#     for mod in modin.readlines():
#         # print type(mod)
#         modify = json.loads(mod.strip())
#         # print type(modify)
#         # print modify
#         change(file, modify)

