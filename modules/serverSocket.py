import socket
import os


def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result
# create a socket object
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = 'localhost'
port = 3000

c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
import socket
import os
import sys
from thread import *

def convert_to_string(no, numBytes):
    result = str(no)
    num = len(result)
    while num < numBytes:
        result = '0' + result
        num += 1
    return result

def clientthread(conn):
        cmd = conn.recv(4)

        if cmd == 'RETR':
            file_name = conn.recv(16)
            print "Nome file dal clien: ", file_name
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

HOST = None               # Symbolic name meaning all available interfaces
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

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
s.close()