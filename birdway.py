# -*- coding: utf-8 -*-
import sys
import socket
import threading
import time
import json
import getopt
import Files
import getip
from random import random


lock = dict()
host_pwd = ''
host_filename = 'log/a.txt'
online_list = list()
cnt = 0


def send(skt, content):
    # if 'newText' in json.loads(content):
    #     print skt, content
    lock[skt].acquire()
    skt.sendall(content + '\n')
    lock[skt].release()


def send_to_all(skt, content, filename):
    for tmp in online_list:
        if tmp != skt and (tmp in Files.editing[filename]):
            send(tmp, content)


def tcp_link(skt, addr):
    syn_time = time.time()
    # try:
    print('Accept new connection from %s:%s...' % addr)
    global cnt
    cnt += 1
    data = ''
    login = 0
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
            # print [data[:pos]]
            msg = json.loads(data[:pos])
            data = data[pos + 1:]

            reply = dict()
            query = msg['type']
            reply['type'] = query
            # if msg['type'] == 'modify':
            #     print msg['newText']

            if query == 'login':
                pwd = msg['pwd']
                if pwd != host_pwd:
                    error = 1
                else:
                    error = 0
                    login = 1
                    online_list.append(skt)
                    Files.add_editor(host_filename, skt)
                    reply['content'] = Files.edit_file(host_filename)
                reply['error'] = error
                send(skt, json.dumps(reply))

            elif login == 0:
                continue

            if query == 'logout':
                login = 0
                break

            elif query == 'modify':
                modify = msg
                print modify
                filename = host_filename
                # print Files.editing[host_filename]
                send_to_all(skt, json.dumps(msg), host_filename)
                print '=========================='
                print Files.edit_file(host_filename)
                Files.change_file(filename, modify)
                print '====>'
                print Files.edit_file(host_filename)
                print '=========================='

            elif query == 'move':
                msg['id'] = cnt
                send_to_all(skt, json.dumps(msg), host_filename)
                # now = time.time()
                # if now - syn_time > 5:
                #     print 'syn'
                #     syn_time = now
                #     reply = dict()
                #     reply['type'] = 'syn'
                #     reply['content'] = Files.edit_file(host_filename)
                #     send(skt, json.dumps(reply))

    save_all()
    Files.del_editor(host_filename, skt)
    online_list.remove(skt)
    skt.close()
    del lock[skt]
    print('Connection from %s:%s closed.' % addr)
    # except:
    #     skt.close()
    #     del lock[skt]
    #     Files.del_editor(host_filename, skt)
    #     online_list.remove(skt)
    #     print('Connection from %s:%s closed.' % addr)


def save_all():
    for filename in Files.file_list:
        Files.save_file(filename)


def save_thread():
    save_time = time.time()
    while True:
        now = time.time()
        if now - save_time > 1:
            save_time = now
            save_all()


def syn_thread():
    # return
    syn_time = time.time()
    while True:
        now = time.time()
        if now - syn_time > 5:
            syn_time = now
            for filename in Files.file_list:
                reply = dict()
                reply['type'] = 'syn'
                reply['content'] = Files.edit_file(filename)
                print reply['content']
                for skt in Files.editing[filename]:
                    send(skt, json.dumps(reply))


def usage():
    print 'birdway.py usage:'
    print '-h, --help: print this help message.'
    print '-f, --file: name of the file which you want to share with others'
    print '-p, --password: set a password for your file, can be omitted'
    print 'For example: birdway.py -f log/a.txt -p 111'


def arg(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hf:p:', ['filename=', 'password='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-p', '--password'):
            global host_pwd
            host_pwd = a
        elif o in ('-f', '--file'):
            global host_filename
            host_filename = a


def main():
    arg(sys.argv)
    if not Files.exist(host_filename):
        print 'No such file'
        sys.exit(3)
    Files.lock[host_filename] = threading.Lock()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = ''
    port = int()
    while True:
        try:
            port = int(random() * 2000 + 2000)
            s.bind((ip, port))
            break
        except:
            pass
    s.listen(10)
    ip = socket.gethostbyname(socket.gethostname())
    print 'Host:', socket.gethostbyname_ex(socket.gethostname())
    print 'Port:', port
    print 'File name:', host_filename
    print 'Password:', host_pwd
    print 'Waiting for connection...'

    t_save = threading.Thread(target=save_thread)
    t_save.setDaemon(True)
    t_save.setName('save_thread')
    t_save.start()
    t_syn = threading.Thread(target=syn_thread)
    t_syn.setDaemon(True)
    t_syn.setName('syn_thread')
    t_syn.start()

    while True:
        sock, addr = s.accept()
        lock[sock] = threading.Lock()
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.setDaemon(True)
        t.start()

    del Files.lock[host_filename]

if __name__ == "__main__":
    # print getip.find_all_ip('Windows')
    main = threading.Thread(target=main)
    main.setDaemon(True)
    main.setName('main_thread')
    main.start()
    while True:
        cin = raw_input()
        if (cin.lower() in ['quit', 'quit()', 'exit()', 'exit', 'break', 'break()']) or not main.isAlive():
            save_all()
            sys.exit(0)
