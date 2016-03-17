import socket
import time
from random import randint
import select
import md5
import hashlib


def recvall(socket, chunk_size):
    data = socket.recv(chunk_size)
    actual_length = len(data)

    while actual_length < chunk_size:
        new_data = socket.recv(chunk_size - actual_length)
        actual_length += len(new_data)
        data += new_data

    return data

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

def get_file(host_ipv4, host_ipv6, host_port, file):

    # TODO: Refactor variabili e metodi
    # TODO: scegliere a random ipv4 e ipv6
    download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: # e' necessario tenere sotto controllo la connessione, perche' puo' disconnettersi il peer o non essere disponibile

        download.connect((host_ipv4,int(host_port)))
        #iodown_socket.setblocking(0)
    except socket.error as e:
        print 'Socket Error: ' + e.message
    else:
        print "Connection with peer enstablished\n"

        download.send("RETR" + file.md5)
        try:
            ack = download.recv(10)
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
                        chunk_length = recvall(download, 5)
                        data = recvall(download, int(chunk_length))
                        fout.write(data)
                    except socket.error as e:
                        print 'Socket Error: ' + e.message
                        break
                    except IOError as e:
                        print 'File error: ' + e.message
                        break
                    except Exception as e:
                        print 'Error: ' + e.message
                        break
                fout.close()
                print 'Download completed'
                print 'Checking file integrity...'
                downloaded_md5 = md5.hashfile(open("shareable/" + fout, 'rb'), hashlib.md5())
                if file.md5 == downloaded_md5:
                    print 'The downloaded file is intact'
                else:
                    print 'Something is wrong. Check the downloaded file'
            else:
                print 'Error: unknown directory response.\n'


def warns_directory(session_id, file_md5, directory):
    # TODO: INSERIRE CONTROLLI!!!!!!!!!!!!!!!!!!!

    cmd = 'GREG' + session_id + file_md5
    directory.sendall(cmd)
    res_msg = directory.recv(14)
    num_down = int(res_msg[4:14])
    if res_msg[0:3] == 'ADRE' and isinstance(num_down, int):
        print 'Other peers downloaded ' + num_down + ' copies of the same file'
    else:
        print 'Error'
