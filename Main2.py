# -*- coding: utf-8 -*-
import socket
import threading
import time
import json
import Users
import Files
import Auth


def send(skt, content):
    skt.sendall(content)


def send_to_all(skt, content, filename):
    for tmp in onlineList:
        if tmp != skt and (tmp in Files.editing[filename]):
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


def tcp_link(skt, addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send(b'Welcome!')
    data = ''
    login = 0
    upload_filename = ''
    while True:
        if not skt:
            break
        data = data + skt.recv(1024)
        # time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break

        # sendToAll(skt, data)
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
                send(skt, json.dumps(reply))

            elif query == 'login':
                username = msg['name']
                u = Users.get_user(username)
                if len(u) < 2:
                    error = 1
                elif u[2] != hash(msg['password']):
                    error = 1
                else:
                    error = 0
                    login = 1
                    onlineList.append(skt)
                    name_list[skt] = username
                reply['error'] = error
                send(skt, json.dumps(reply))

            elif login == 0:
                continue

            if query == 'logout':
                login = 0
                onlineList.remove(skt)
                break

            elif query == 'create':
                filename = msg['filename']
                error = Files.create_file(filename)
                reply['error'] = error
                if error == 0:
                    Auth.change(filename, name_list[skt], 2, name_list[skt])
                send(skt, json.dumps(reply))

            elif query == 'edit':
                filename = msg['filename']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(skt, json.dumps(reply))
                    continue
                if not Auth.have_edit_auth(filename, name_list[skt]):
                    reply['error'] = 2
                    send(skt, json.dumps(reply))
                    continue
                reply['error'] = 0
                send(skt, json.dumps(reply))
                reply.clear()
                reply['type'] = 'edit_content'
                reply['filename'] = 'filename'
                reply['isend'] = 1
                content = dict()
                content['oldRange'] = {'start': {'row': 0, 'column': 0}, 'end': {'row': 0, 'column': 0}}
                content['oldText'] = ''
                (file_content, r, c) = Files.edit_file(filename)
                content['newText'] = file_content
                content['newRange'] = {'start': {'row': 0, 'column': 0}, 'end': {'row': r, 'column': c}}
                reply['content'] = content
                send(skt, json.dump(reply))

                Files.add_editor(filename, skt)

            elif query == 'upload':
                filename = msg['filename']
                error = Files.create_file(filename)
                reply['error'] = error
                send(skt, json.dumps(reply))
                if error == 1:
                    continue
                upload_filename = filename
                Auth.change(filename, name_list[sock], 2, name_list[skt])

            elif query == 'upload_content':
                if upload_filename == '':
                    continue
                Files.up_file(upload_filename, msg['content']['newText'])
                upload_filename = ''
                pass

            elif query == 'change_auth':
                filename = msg['filename']
                other_name = msg['other_name']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(skt, json.dumps(reply))
                    continue
                if not Auth.have_manage_auth(filename, other_name):
                    reply['error'] = 2
                    send(skt, json.dumps(reply))
                    continue
                reply['error'] = 0
                Auth.change(filename, other_name, msg['auth'])
                send(skt, json.dumps(reply))
                pass

            elif query == 'rm':
                filename = msg['filename']
                if not Files.exist(filename):
                    reply['error'] = 1
                    send(skt, json.dumps(reply))
                    continue
                if not Auth.have_manage_auth(filename, name_list[skt]):
                    reply['error'] = 2
                    send(skt, json.dumps(reply))
                    continue
                reply['error'] = 0
                Files.delete_file(filename)
                send(skt, json.dumps(reply))

            elif query == 'ls':
                reply['list'] = Auth.get_edit_list(name_list[skt])
                send(skt, json.dumps(reply))
                pass

            elif query == 'close':
                Files.del_editor(msg['filename'], skt)

            elif query == 'modify':
                modify = msg['content']
                filename = msg['filename']
                send_to_all(skt, json.dumps(modify), filename)
                Files.change_file(filename, modify)

    skt.close()
    print('Connection from %s:%s closed.' % addr)


def save_thread():
    while True:
        if time.time() - init_time > 10:
            for filename in Files.file_list:
                Files.save_file(filename)
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 2333
s.bind((ip, port))
s.listen(5)
print 'Host:', ip + ':' + str(port)
print 'Waiting for connection...'
onlineList = []
name_list = ['' for i in range(100)]
init_time = time.time()
threading.Thread(target=save_thread)
while True:
    sock, addr = s.accept()
    onlineList.append(sock)
    t = threading.Thread(target=tcp_link, args=(sock, addr))
    t.start()


