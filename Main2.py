# -*- coding: utf-8 -*-
import socket
import threading
import time
import json
import Users
import Files
import Auth


def send(sock, str):
    sock.send(str)


def send_to_all(sock, content, filename):
    for tmp in onlineList:
        if tmp != sock:
            send(tmp, content)

# def findEnter(str):
#     l = len(str)
#     ct = 0
#     for i in range(0,l):
#         if str[i] == '{':
#             ct += 1
#         elif str[i] == '}':
#             ct -= 1
#         elif str[i] == '\n' and ct == 0:
#             return i
#     return -1


def tcp_link(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send(b'Welcome!')
    data = ''
    fileNo = 0
    login = 0
    upload_filename = ''
    while True:
        if not sock:
            break
        data = data + sock.recv(1024)
        # time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break

        # sendToAll(sock, data)
        # data = ''
        while True:
            try:
                pos = data.index('\n')
            except:
                break
            print [data[:pos]]
            msg = json.loads(data[:pos])

            reply = dict()
            query = msg['type']
            reply['type'] = query

            if query == 'register':
                error = Users.insert_user(msg['user'], msg['password'])
                reply['error'] = error
                send(sock, json.dumps(reply))

            elif query == 'login':
                username = msg['name']
                u = Users.get_user(username)
                if len(u) < 2:
                    error = 1
                else:
                    error = 0
                    login = 1
                    onlineList.append(sock)
                    name_list[sock] = username
                reply['error'] = error
                send(sock, json.dumps(reply))

            elif login == 0:
                continue

            if query == 'logout':
                login = 0
                onlineList.remove(sock)
                break

            elif query == 'create':
                filename = msg['filename']
                error = Files.create_file(filename)
                reply['error'] = error
                send(sock, json.dumps(reply))

            elif query == 'edit':
                filename = msg['filename']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(sock, json.dumps(reply))
                    continue
                if not Auth.have_edit_auth(filename, name_list[sock]):
                    reply['error'] = 2
                    send(sock, json.dumps(reply))
                    continue
                reply['error'] = 0
                send(sock, json.dumps(reply))
                reply.clear()
                reply['type'] = 'edit_content'
                reply['filename'] = 'filename'
                reply['isend'] = 1
                content = dict()
                content['oldRange'] = {'start': {'row': 0, 'column': 0}, 'end': {'row': 0, 'column': 0}}
                content['oldText'] = ''
                (file_content, r, c) = Files.get_file_string(filename)
                content['newText'] = file_content
                content['newRange'] = {'start': {'row': 0, 'column': 0}, 'end': {'row': r, 'column': c}}
                reply['content'] = content
                send(sock, json.dump(reply))

            elif query == 'upload':
                filename = msg['filename']
                error = Files.create_file(filename)
                reply['error'] = error
                send(sock, json.dumps(reply))
                if error == 1:
                    continue
                upload_filename = filename

            elif query == 'upload_content':
                if upload_filename == '':
                    continue
                Files.up_file(name=upload_filename, content=msg['content']['newText'])
                pass

            elif query == 'change_auth':
                filename = msg['filename']
                other_name = msg['other_name']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(sock, json.dumps(reply))
                    continue
                if not Auth.have_manage_auth(filename, other_name):
                    reply['error'] = 2
                    send(sock, json.dumps(reply))
                    continue
                reply['error'] = 0
                Auth.change(filename, other_name, msg['auth'])
                send(sock, json.dumps(reply))
                pass

            elif query == 'rm':
                filename = msg['filename']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(sock, json.dumps(reply))
                    continue
                if not Auth.have_manage_auth(filename, name_list[sock]):
                    reply['error'] = 2
                    send(sock, json.dumps(reply))
                    continue
                reply['error'] = 0
                Files.delete_file(filename)
                send(sock, json.dumps(reply))

            elif query == 'ls':
                reply['list'] = Auth.get_edit_list(name_list[sock])
                send(sock, json.dumps(reply))
                pass

            elif query == 'now_file':
                pass

            elif query == 'modify':
                modify = msg['content']
                filename = msg['filename']
                send_to_all(sock, json.dumps(modify), filename)
                Files.changeFile(filename, modify)

    sock.close()
    print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2333))
s.listen(5)
print('Waiting for connection...')
onlineList = []
name_list = ['' for i in range(100)]
while True:
    sock, addr = s.accept()
    onlineList.append(sock)
    t = threading.Thread(target=tcp_link, args=(sock, addr))
    t.start()


