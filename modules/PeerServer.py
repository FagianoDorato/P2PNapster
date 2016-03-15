import socket
import threading
import os
from modules import SharedFile
import PeerHandler


class PeerServer(threading.Thread):
    peerserver_socket = None
    peerserver_ipv4 = None
    peerserver_ipv6 = None
    peerserver_port = None
    filesList = None
    allow_run = True

    def __init__(self, ipv4, ipv6, port, fileList):
        threading.Thread.__init__(self)

        self.peerserver_ipv4 = ipv4
        self.peerserver_ipv6 = ipv6
        self.peerserver_port = port
        self.filesList = fileList

    def run(self):
        self.peerserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peerserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peerserver_socket.bind((self.peerserver_ipv4, int(self.peerserver_port)))
        self.peerserver_socket.listen(5)
        #print "listening for peers on " + self.peerserver_ipv4 + " " + self.peerserver_port
        try:
            while self.allow_run:
                try:
                    conn, addr = self.peerserver_socket.accept()
                    print 'Peer connected on: ', addr

                    peer = PeerHandler.PeerHandler(conn, addr, self.fileList)
                    peer.start()
                except Exception:
                    print "Error"
                finally:
                    conn.close()
        finally:
            conn.close()



    def stop(self):
        self.allow_run = False