import socket
import time
from random import randint
import md5
import hashlib
import Connection


def recvall(socket, chunk_size):
    data = socket.recv(chunk_size)
    actual_length = len(data)

    while actual_length < chunk_size:
        new_data = socket.recv(chunk_size - actual_length)
        actual_length += len(new_data)
        data += new_data

    return data


def get_file(session_id, host_ipv4, host_ipv6, host_port, file, directory):

    # TODO: Refactor variabili e metodi
    # TODO: scegliere a random ipv4 e ipv6
    c = Connection.Connection(host_ipv4, host_ipv6, host_port)
    c.connect()
    download = c.socket

    msg = 'RETR' + file.md5
    print 'Download Message: ' + msg
    try:
        download.send(msg)
        print 'Message sent, waiting for response...'
        response_message = download.recv(10)
    except socket.error as e:
        print 'Error: ' + e.message
    except Exception as e:
        print 'Error: ' + e.message
    else:
        if response_message[:4] == 'ARET':
            n_chunks = response_message[4:10]

            filename = file.name
            fout = open('received/' + filename, "ab")

            n_chunks = str(n_chunks).lstrip('0')

            for i in range(0, int(n_chunks)):
                print 'Chunk n' + str(i)
                try:
                    chunk_length = recvall(download, 5)
                    data = recvall(download, int(chunk_length))
                    fout.write(data)
                except socket.error as e:
                    print 'Socket Error: ' + e.message
                    break
                except IOError as e:
                    print 'IOError: ' + e.message
                    break
                except Exception as e:
                    print 'Error: ' + e.message
                    break
            fout.close()
            print 'Download completed'

            warns_directory(session_id, file.md5, directory)
            print 'Checking file integrity...'
            downloaded_md5 = md5.hashfile(open("received/" + fout.name, 'rb'), hashlib.md5())
            if file.md5 == downloaded_md5:
                print 'The downloaded file is intact'
            else:
                print 'Something is wrong. Check the downloaded file'
        else:
            print 'Error: unknown response from directory.\n'

def warns_directory(session_id, file_md5, directory):
    cmd = 'DREG' + session_id + file_md5
    try:
        directory.sendall(cmd)
        print 'Message sent, waiting for response...'
        response_message = directory.recv(14)
        print 'Directory responded: ' + response_message
    except socket.error as e:
        print 'Socket Error: ' + e.message
    except Exception as e:
        print 'Error: ' + e.message

    num_down = int(response_message[4:14])
    if response_message[0:3] == 'ADRE' and isinstance(num_down, int):
        print 'Other peers downloaded ' + num_down + ' copies of the same file'
    else:
        print 'Error: unknown response from directory.\n'
