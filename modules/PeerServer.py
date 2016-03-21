import socket
import threading
import os
from modules import SharedFile
import PeerHandler
import Connection

class PeerServer(threading.Thread):
    peerserver_socket = None
    peerserver_ipv4 = None
    peerserver_ipv6 = None
    peerserver_port = None
    fileList = None
    allow_run = True
    threads = []

    def __init__(self, ipv4, ipv6, port, fileList):
        threading.Thread.__init__(self)

        self.peerserver_ipv4 = ipv4
        self.peerserver_ipv6 = ipv6
        self.peerserver_port = port
        self.fileList = fileList

    def run(self):
        c = Connection.Connection(self.peerserver_ipv4, self.peerserver_ipv6, self.peerserver_port)
        c.listen()
        self.peerserver_socket = c.socket
        #self.peerserver_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        #self.peerserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.peerserver_socket.bind((self.peerserver_ipv6, int(self.peerserver_port)))
        #self.peerserver_socket.listen(5)

        try:
            while self.allow_run:
                try:
                    conn, addr = self.peerserver_socket.accept()
                    print 'Peer connected on: ', addr

                    peer = PeerHandler.PeerHandler(conn, addr, self.fileList)
                    peer.start()
                    self.threads.append(peer)
                except Exception as e:
                    print "Error: "+Exception+" / " + e.message
        except Exception as e:
            print 'Error: ' + e.message
        #finally:
        #    conn.close()

    def stop(self):
        self.allow_run = False

        for p in self.threads:
            p.join()

        self.peerserver_socket.close()