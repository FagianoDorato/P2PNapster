import socket
import os
import sys
from thread import *
from multiprocessing import Process

def convert_to_string(no, numBytes):
    result = str(no)
    num = len(result)
    while num < numBytes:
        result = '0' + result
        num += 1
    return result

def clientthread(conn):
        #manca controllo lista per reperimento file da sharable

        cmd = conn.recv(4)
        if cmd == 'RETR':
            file_name = conn.recv(16)
            print "Nome file dal client: ", file_name
            if os.path.exists(file_name):
                length = os.path.getsize(file_name)
            length = os.stat(file_name).st_size
            print "Lunghezza file", length
            numChunks = length / 1024 + 1

            strChunks = convert_to_string(numChunks, 6)
            conn.send('ARET')
            conn.send(strChunks)
            with open(file_name, 'rb') as f:
                l = f.read(1024)
                while (l):
                    lenChunk = len(str(l))
                    strLenChunk = convert_to_string(lenChunk, 5)
                    conn.send(strLenChunk)
                    conn.send(l)
                    l = f.read(1024)

def start_server():
    #creo un nuvo processo in ascolto delle richieste dei peer
    newpid = os.fork()
    if newpid == 0:              #sono nel processo figlio
        HOST = None               # Symbolic name meaning all available interfaces
        PORT = 3000              # Arbitrary non-privileged port
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET6,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                continue
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(sa)
                s.listen(5)
            except socket.error as msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print 'could not open socket'
            sys.exit(1)

        while True:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            print 'Connected by', addr

            #start new thread takes 1st argument as a function name to be run
            start_new_thread(clientthread ,(conn,))
        s.close()
    else:
        return newpid #per chiudere il processo del server al logout


def start_server_multithread():

    print "initializing server multithread"
    HOST = None            # Symbolic name meaning all available interfaces
    PORT = 3000              # Arbitrary non-privileged port
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(sa)
            s.listen(5)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print 'could not open socket'
        sys.exit(1)

    while True:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected by', addr

        #thread = threading.Thread(target=clientthread)
        #thread.start()
        #print "starter thread"
        #thread.joint()

        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        #start_new_thread(clientthread, (conn, lista_file))
    s.close()