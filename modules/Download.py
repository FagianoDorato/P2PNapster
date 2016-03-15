import socket
from random import randint

def get_file(hostIpv4, hostIpv6, port, file):

    PORT = port
    if randint(0,1) == 0:
        HOST = hostIpv4
    else:
        HOST = hostIpv6

    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        return 'could not open socket'

    cmd = 'RETR' + file.md5
    s.sendall(cmd)

    r = s.recv(4)
    if r != 'ARET':
        s.close()
        return "Error ARET from Peer"
    numChunks = int(s.recv(6))

    f = open('shareable/' + file.name, 'wb')
    recvd = ''
    while numChunks > 0:
        print '',numChunks
        lenChunk = int(s.recv(5))
        data = s.recv(lenChunk)
        if not data:
            break
        recvd += data
        numChunks -= 1

    f.write(recvd)
    f.close()
    s.close()
    return "OK"

def warns_directory(sessionId, file_md5, connToDir):
    cmd = 'GREG' + sessionId + file_md5
    connToDir.socketDirectory.sendall(cmd)
    res_msg = connToDir.soketDirectory.recv(14)
    numDown = int(res_msg[4:14])
    if res_msg[0:3] == 'ADRE' and isinstance( numDown, int ):
        return 'Gli altri peer hanno scaricato ', numDown, ' copie dello stesso file!'
    else:
        return 'Errore nella risposta dalla directory!'