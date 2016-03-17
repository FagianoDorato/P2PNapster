import threading


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

        ### calcolo della dimensione del file

        F = open(n,'r')
        F.seek(0,2)
        sz = F.tell()
        F.seek(0,0)
        F.close()
        return sz
        # end of filesize method

    def run(self):

        cmd = self.conn.recv(4)
        print cmd
        if cmd == "RETR":
            self.md5 = self.conn.recv(16)

            found_name = None
            for idx, file in enumerate(self.fileList):
                if file.md5 == self.md5:
                    found_name = file.name

            chunk_dim = 2048
            try:
                file = open("shareable/" + found_name, "rb")
            except Exception, expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer " + self.addrclient[0] + "\n"
            else:
                tot_dim = self.filesize("shareable/" + found_name)
                num_of_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                resto = tot_dim % chunk_dim #eventuale resto della divisione
                if resto != 0.0:
                    num_of_chunks+=1

                num_chunks_form = '%(#)06d' % {"#" : int(num_of_chunks)}
                file.seek(0, 0)
                try :
                    buff = file.read(chunk_dim)
                    chunk_sent = 0
                    self.conn.sendall("ARET" + num_chunks_form)
                    while len(buff) == chunk_dim :
                        chunk_dim_form = '%(#)05d' % {"#" : len(buff)}
                        try:
                            self.conn.sendall(str(chunk_dim_form) + buff)
                            chunk_sent = chunk_sent +1
                            buff = file.read(chunk_dim)
                        except IOError:
                            print "Connection error due to the death of the peer!!!\n"
                    if len(buff) != 0:
                        chunk_last_form = '%(#)05d' % {"#" : len(buff)}
                        self.conn.sendall(chunk_last_form + buff)
                    print "Upload Completed"
                    file.close()
                except EOFError:
                    print "You have read a EOF char"
        else:
            print "Error: unknown directory response.\n"

        self.conn.shutdown(1)
        self.conn.close()