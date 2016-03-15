import socket
import json
import SharedFile
import os
import hashlib
from random import randint


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()


#TCP_IP = '172.30.8.1'#'127.0.0.1'
#TCP_IP = 'fc00::8:1'
TCP_IP = None
#TCP_IP = '::1'
TCP_PORT = 3000
BUFFER_SIZE = 20

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)
#
# conn, addr = s.accept()
for res in socket.getaddrinfo(TCP_IP, TCP_PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
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
#print 'Connection address:', addr
while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    cmd = conn.recv(4)

    if cmd == "FIND":
        print "received command: " + str(cmd)
        sessionId = conn.recv(16)
        print "received sessionID: " + str(sessionId)
        term = conn.recv(20)
        print "received search term: " + str(term)


        #  Finta risposta dalla directory
        #  Number of different md5
        idmd5 = None

        response = 'AFIN' + str(4).zfill(3)

        for root, dirs, files in os.walk("../shareable"):
            for file in files:
                filemd5 = hashfile(open("../shareable/" + file, 'rb'), hashlib.md5())
                filename = file.ljust(100)
                copies = str(2).zfill(3)
                response += filemd5
                response += filename
                response += copies  # 2 copie
                response += '172.030.008.001|fc00:0000:0000:0000:0000:0000:0008:0001'
                response += '03000'
                response += '172.030.008.003|fc00:0000:0000:0000:0000:0000:0008:0003'
                response += '03000'

        conn.send(response)

    elif cmd == "LOGI":
        print "received command: " + str(cmd)
        ipv4 = conn.recv(16).replace("|", "")  # ipv4
        print "received ipv4: " + str(ipv4)
        ipv6 = conn.recv(39)
        print "received ipv6: " + str(ipv6)
        port = conn.recv(5)
        print "received porta: " + str(port)
        print 'messaggio ricevuto da Peer: ' + 'AFIN' + '1234567891234567'
        response = 'AFIN' + '1234567891234567'
        print response
        conn.send(response)

    elif cmd == 'LOGO':
        print "received command: " + str(cmd)
        sessionid = conn.recv(16)
        print "peer: " + sessionid
        response = 'ALGO' + '003'
        print response
        conn.send(response)

    elif cmd == 'ADDF':
        response = 'RADD' + '003'
        print response
        conn.send(response)

    elif cmd == 'DELF':
        response = 'RDEL' + '003'
        print response
        conn.send(response)

    elif cmd == 'RETR':
        file_name = conn.recv(16)
        print "Nome file dal client: ", file_name
        if os.path.exists(file_name):
            length = os.path.getsize(file_name)
        length = os.stat(file_name).st_size
        print "Lunghezza file", length
        numChunks = length / 1024 + 1

        strChunks = numChunks.zfill(6)
        conn.send('ARET')
        conn.send(strChunks)
        with open(file_name, 'rb') as f:
            l = f.read(1024)
            while (l):
                lenChunk = len(str(l))
                strLenChunk = lenChunk.zfill(5)
                conn.send(strLenChunk)
                conn.send(l)
                l = f.read(1024)