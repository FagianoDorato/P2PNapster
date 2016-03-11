import socket

def get_file(host, port, file_md5):

    s = socket.socket()
    s.connect((host, port))

    cmd = 'RETR' + file_md5
    s.sendall(cmd)

    r = s.recv(4)
    if r != 'ARET':
        s.close()
        return "Errone ARET from Peer"
    numChunks = int(s.recv(6))
    # uso md5 come nome del file
    f = open('shareable/' + file_md5, 'wb')
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

def warns_directory():
    pass