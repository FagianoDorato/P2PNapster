import socket

s = socket.socket()
s.connect(('localhost', 3000))

def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res
def get_file(s, file_name):
    cmd = 'RETR' + file_name
    s.sendall(cmd)

    r = s.recv(4)
    print r
    size = int(s.recv(16))
    recvd = ''
    while size > len(recvd):
        data = s.recv(1024)
        if not data:
            break
        recvd += data
    return recvd

print get_file(s, 'shareable/prova')
