# -*- coding: utf-8 -*-
import socket
import threading
import time
import json
import Users
import Files


def send(sock, str):
    sock.send(str)


def send_to_all(sock, str):
    for tmp in onlineList:
        if tmp != sock:
            send(tmp, str)

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

            if not ("type" in msg):
                pass
            else:
                type = msg['type']
                if type == 'register':
                    pass
                elif type == 'login':
                    pass
                elif type == 'create':
                    pass
                elif type == 'edit':
                    pass
                elif type == 'upload':
                    pass
                elif type == 'upload_content':
                    pass
                elif type == 'change_auth':
                    pass
                elif type == 'rm':
                    pass
                elif type == 'ls':
                    pass
                elif type == 'now_file':
                    pass

            send_to_all(sock, data[:pos + 1])   #
            data = data[pos + 1:]
            # print data
            Files.changeFile(fileNo, modify)

    onlineList.remove(sock)
    sock.close()
    print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2333))
s.listen(5)
print('Waiting for connection...')
onlineList = []
while True:
    sock, addr = s.accept()
    onlineList.append(sock)
    t = threading.Thread(target=tcp_link, args=(sock, addr))
    t.start()


