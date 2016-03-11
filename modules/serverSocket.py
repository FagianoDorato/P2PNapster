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
# bind to the port
c.bind((host, port))
# queue up to 5 requests
c.listen(5)
s,a = c.accept()


while True:
    cmd = s.recv(4)
    print "Comando ricevuti " + cmd

    if cmd == 'RETR':
        file_name = s.recv(16)
        if os.path.exists(file_name):
            length = os.path.getsize(file_name)

        numChunks = length / 1024 + 1

        byteChunks = convert_to_bytes(numChunks)
        print "Numero chunks", len(str(numChunks))
        with open(file_name, 'rb') as f:
            l = f.read(1024)
            while (l):
                print l

                l = f.read(1024)



        #s.sendall('%16d' % len(data))
        s.sendall('ARET')
        s.recv(2)
