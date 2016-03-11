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


TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:

    response = 'ADEL' + str(993).zfill(3)
    print response
    conn.send(response)

conn.close()

'''
cmd = conn.recv(4)

    if not cmd: break
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
            print copies
            response += filemd5
            response += filename
            response += copies  # 2 copie
            response += '172.030.008.001|fc00:0000:0000:0000:0000:0000:0008:0001'
            response += '03000'
            response += '172.030.008.002|fc00:0000:0000:0000:0000:0000:0008:0002'
            response += '03000'
            '''