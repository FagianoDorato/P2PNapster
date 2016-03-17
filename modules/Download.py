import socket
import time
from random import randint
import select

def recvall(socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

    lettiTot = socket.recv(numToRead)
    num = len(lettiTot)

    while (num < numToRead):
        letti = socket.recv(numToRead - num)
        num = num + len(letti)
        lettiTot = lettiTot + letti

    return lettiTot #restituisco la stringa letta
    # end of recvall method

'''
def recvall(sock, buffer_size):
    buf = sock.recv(buffer_size)
    while buf:
        yield buf
        buf = sock.recv(buffer_size)
'''
'''
def recvall2(sock, buffer_size):
    buf = b''
    while buffer_size:
        newbuf = sock.recv(buffer_size)
        if not newbuf: return None
        buf += newbuf
        buffer_size -= len(newbuf)
    return buf
'''
'''
def get_file(hostIpv4, hostIpv6, port, file):

    PORT = port
    if True:
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

    f = open('received/' + file.name, 'wb')
    #   f = open('shareable/' + file.name, 'wb')
    recvd = ''
    while numChunks > 0:
        print '',numChunks
        r = s.recv(5)
        if r != '01024':
            print "eccolo"
        lenChunk = int(r)
        data = s.recv(lenChunk)
        if not data:
            break
        recvd += data
        numChunks -= 1

    f.write(recvd)
    f.close()
    s.close()
    return "OK"
'''

def get_file(hostIpv4, hostIpv6, port, file):

    # TODO: scegliere a random ipv4 e ipv6
    iodown_host = hostIpv4
    iodown_port = int(port)
    iodown_addr = (iodown_host, iodown_port)
    iodown_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: # e' necessario tenere sotto controllo la connessione, perche' puo' disconnettersi il peer o non essere disponibile

        iodown_socket.connect(iodown_addr)
        #iodown_socket.setblocking(0)
    except IOError: #IOError exception includes socket.error
        print "Connection with " + hostIpv4 + "not available"
    else:
        print "Connection with peer enstablished.\n"
        #print "Download will start shortly! Be patient"

        # SPEDISCO IL PRIMO MESSAGGIO
        iodown_socket.send("RETR" + file.md5)

        try:
            # Acknowledge "ARET" dal peer
            #ack = iodown_socket.recv(10)
            ack = iodown_socket.recv(10)
        except IOError as e:
            print "Error: " + e.message
        else:

            if ack[:4] == 'ARET':
                num_chunk = ack[4:10]

                filename = file.name
                fout = open('received/' + filename, "ab")

                num_chunk_clean = str(num_chunk).lstrip('0')

                for i in range(0, int(num_chunk_clean)):
                    print 'Chunk n°' + int(i)
                    try:
                        lungh_form = recvall(iodown_socket, 5)
                        lungh = int(lungh_form)

                        data = recvall(iodown_socket, lungh)
                        #time.sleep(0.005)
                        #recvd += data
                        fout.write(data)
                    except IOError, expt:
                        print "Connection or File-access error -> %s" % expt
                        break
                fout.close()
                print "Download Completato"


def warns_directory(sessionId, file_md5, connToDir):
    cmd = 'GREG' + sessionId + file_md5
    connToDir.socketDirectory.sendall(cmd)
    res_msg = connToDir.soketDirectory.recv(14)
    numDown = int(res_msg[4:14])
    if res_msg[0:3] == 'ADRE' and isinstance(numDown, int):
        print 'Gli altri peer hanno scaricato ' + numDown + ' copie dello stesso file'
    else:
        print 'Errore nella risposta dalla directory'