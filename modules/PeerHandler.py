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

    def run(self):

        # TODO: gestire errori ed exception
        cmd = self.conn.recv(4)
        print cmd
        if cmd == "RETR":

            self.md5 = self.conn.recv(16)

            found_name = None

            for idx, file in self.fileList:
                if file.md5 == self.md5:
                    found_name = file.name

            # TODO: controllare found name
            if os.path.exists(found_name):
                length = os.path.getsize(found_name)
            length = os.stat(found_name).st_size
            print "Lunghezza file", length
            numChunks = length / 1024 + 1
            self.conn.send("ARET" + numChunks.zfill(6))

            with open(found_name, 'rb') as f:
                l = f.read(1024)
                while (l):
                    lenChunk = len(str(l))
                    self.conn.send(lenChunk.zfill(5))
                    self.conn.send(l)
                    l = f.read(1024)

            f.close()

        self.conn.close()