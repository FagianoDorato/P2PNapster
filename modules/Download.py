import socket
import time
from random import randint
import select

def sockread(socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

    lettiTot = socket.recv(numToRead)
    num = len(lettiTot)

    while (num < numToRead):
        letti = socket.recv(numToRead - num)
        num = num + len(letti)
        lettiTot = lettiTot + letti

    return lettiTot #restituisco la stringa letta
    # end of sockread method


def recvall(sock, buffer_size):
    buf = sock.recv(buffer_size)
    while buf:
        yield buf
        buf = sock.recv(buffer_size)


def recvall2(sock, buffer_size):
    buf = b''
    while buffer_size:
        newbuf = sock.recv(buffer_size)
        if not newbuf: return None
        buf += newbuf
        buffer_size -= len(newbuf)
    return buf


def get_file(hostIpv4, hostIpv6, port, file):
    print file.name
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

    r = s.recv(10)
    if r[0:4] != 'ARET':
        s.close()
        return "Error ARET from Peer"
    numChunks = int(r[4:10])

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


def get_file2(hostIpv4, hostIpv6, port, file):

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
        except IOError:
            print "Connection error. The peer " + hostIpv4 + " is death\n"
        else:

            if ack[:4]=="ARET":


                num_chunk = ack[4:10]

                #filename = file.name
                filename = "cisco.pdf"
                fout = open('received/' + filename, "ab") #a di append, b di binary mode


                #pulisco il numero di chunks dagli 0
                num_chunk_clean = str(num_chunk).lstrip('0')

                #print "The number of chunks is " + num_chunk_clean + "\n"
                recvd = ''

                #rsock, _, _= select.select([iodown_socket], [], [])

                data = []
                datalength = []
                #if rsock:
                    #rsock = rsock[0]
                rsock = iodown_socket
                for i in range(0,int(num_chunk_clean)): #i e' il numero di chunk
                    print int(i)


                    #print "Watching chunk number " + str(int(i+1))

                    #devo leggere altri byte ora
                    #ne leggo 5 perche' 5 sono quelli che mi diranno poi quanto e' lungo il chunk
                    try:

                        #lungh_form = iodown_socket.recv(5) #ricevo lunghezza chunck formattata
                        #lungh_form = rsock.recv(5)
                        #print lungh_form
                        datalength.append(recvall2(rsock, 5))
                        lungh = int(datalength[-1]) #converto in intero
                        print lungh

                        #devo leggere altri byte ora
                        #ne leggo lungh perche' quella e' proprio la lunghezza del chunk

                        #data = iodown_socket.recv(lungh)
                        data.append(recvall2(rsock, lungh))
                        '''while len(data) < int(lungh_form):
                            data_overflow = iodown_socket.recv(int(lungh_form) - len(data))
                            data += data_overflow'''
                        #time.sleep(0.005)

                        #print "ho ricevuto i byte" #TODO debug mode

                        #recvd += data
                        #lo devo mettere sul mio file che ho nel mio pc

                        #fout.write(data) #scrivo sul file in append

                        #print ""

                    except IOError, expt:

                        print "Connection or File-access error -> %s" % expt
                        break
                #ho finito di ricevere il file
                result = b''.join(data)
                fout.write(result)
                fout.close()
                print "finito di scrivere!" #chiudo il file perche' ho finito di scaricarlo


def warns_directory(sessionId, file_md5, connToDir):
    cmd = 'GREG' + sessionId + file_md5
    connToDir.socketDirectory.sendall(cmd)
    res_msg = connToDir.soketDirectory.recv(14)
    numDown = int(res_msg[4:14])
    if res_msg[0:3] == 'ADRE' and isinstance( numDown, int ):
        return 'Gli altri peer hanno scaricato ', numDown, ' copie dello stesso file!'
    else:
        return 'Errore nella risposta dalla directory!'