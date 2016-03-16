import socket
import os
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

        # TODO: gestire errori ed exception
        cmd = self.conn.recv(4)
        print cmd
        if cmd == "RETR":

            self.md5 = self.conn.recv(16)

            found_name = None

            for idx, file in enumerate(self.fileList):
                if file.md5 == self.md5:
                    found_name = file.name

            # TODO: controllare found name
            found_name = "cisco.pdf"
            # if os.path.exists(found_name):
            #     length = os.path.getsize(found_name)
            # length = os.stat("shareable/" + found_name).st_size
            # print "Lunghezza file", length
            # numChunks = length / 128 + 1
            # self.conn.send("ARET" + str(numChunks).zfill(6))
            #
            # with open("shareable/" + found_name, 'rb') as f:
            #     l = f.read(1024)
            #     while l:
            #         lenChunk = len(str(l))
            #         self.conn.send(str(lenChunk).zfill(5))
            #         self.conn.send(l)
            #         l = f.read(1024)
            #
            # f.close()
            chunk_dim = 1024
            try :
                file = open("shareable/" + found_name, "rb")
            except Exception,expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer " + self.addrclient[0] + "\n"
            else :
                tot_dim=self.filesize("shareable/" + found_name)
                num_of_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                resto = tot_dim % chunk_dim #eventuale resto della divisione
                if resto != 0.0:
                    num_of_chunks+=1

                num_chunks_form = '%(#)06d' % {"#" : int(num_of_chunks)}

                print num_chunks_form
                file.seek(0,0) #sposto la testina di lettura ad inizio file
                try :
                    buff = file.read(chunk_dim)
                    chunk_sent = 0
                    self.conn.sendall("ARET" + num_chunks_form)
                    while len(buff) == chunk_dim :
                        chunk_dim_form = '%(#)05d' % {"#" : len(buff)}
                        try:

                            #print chunk_dim_form
                            self.conn.sendall(str(chunk_dim_form) + buff)
                            chunk_sent = chunk_sent +1
                            print "sent" + str(chunk_sent)
                            #print "Sent " + str(chunk_sent) + " chunks to " + str(self.addrclient[0])#TODO debug
                            buff = file.read(chunk_dim)
                        except IOError: #this exception includes the socket.error child!
                            print "Connection error due to the death of the peer!!!\n"
                    if len(buff) != 0:
                        #print "coda del file" #TODO debug
                        chunk_last_form = '%(#)05d' % {"#" : len(buff)}
                        self.conn.sendall(chunk_last_form + buff)
                    print "End of upload of " + found_name
                    file.close()
                    #print "ho chiuso il file" #TODO debug
                except EOFError:
                    print "You have read a EOF char"

        self.conn.close()