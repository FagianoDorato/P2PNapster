import threading
import socket

class PeerHandler(threading.Thread):
    conn = None
    addr = None
    fileList = None
    md5 = None

    def __init__(self, conn, addr, fileList):
        threading.Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.fileList = fileList

    def filesize(self, n):
        F = open(n,'r')
        F.seek(0,2)
        sz = F.tell()
        F.seek(0,0)
        F.close()
        return sz

    def run(self):

        try:
            cmd = self.conn.recv(4)
        except socket.error as e:
            print 'Socket Error: ' + e.message
        except Exception as e:
            print 'Error: ' + e.message
        else:
            if cmd == "RETR":
                try:
                    self.md5 = self.conn.recv(32)
                    print 'Received md5: ' + self.md5
                except socket.error as e:
                    print 'Socket Error: ' + e.message
                except Exception as e:
                    print 'Error: ' + e.message
                else:
                    found_name = None

                    for idx, file in enumerate(self.fileList):
                        if file.md5 == self.md5:
                            found_name = file.name

                    if found_name is None:
                        print 'Found no file with md5: ' + self.md5
                    else:
                        chunk_dim = 2048
                        try:
                            file = open("shareable/" + found_name, "rb")
                        except Exception as e:
                            print 'Error: ' + e.message + "\n"
                        else:
                            tot_dim = self.filesize("shareable/" + found_name)
                            num_of_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                            resto = tot_dim % chunk_dim #eventuale resto della divisione
                            if resto != 0.0:
                                num_of_chunks += 1

                            file.seek(0, 0)
                            try:
                                buff = file.read(chunk_dim)
                                chunk_sent = 0

                                msg = 'ARET' + str(num_of_chunks).zfill(6)
                                print 'Upload Message: ' + msg
                                self.conn.sendall(msg)
                                print 'Sending chunks...'

                                while len(buff) == chunk_dim:
                                    try:
                                        msg = str(len(buff)).zfill(5) + buff
                                        self.conn.sendall(msg)
                                        chunk_sent += 1
                                        print 'Sent ' + chunk_sent
                                        buff = file.read(chunk_dim)
                                    except IOError:
                                        print "Connection error due to the death of the peer!!!\n"
                                if len(buff) != 0:
                                    msg = str(len(buff)).zfill(5) + buff
                                    self.conn.sendall(msg)
                                print "Upload Completed"
                                file.close()
                            except EOFError:
                                print "You have read a EOF char"
            else:
                print "Error: unknown directory response.\n"

        self.conn.shutdown(1)
        self.conn.close()