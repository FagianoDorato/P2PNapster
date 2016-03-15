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

    def __init__(self, ipv4, ipv6, port, fileList):
        threading.Thread.__init__(self)

        self.peerserver_ipv4 = ipv4
        self.peerserver_ipv6 = ipv6
        self.peerserver_port = port
        self.filesList = fileList


    def run(self):

        self.peerserver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peerserver_socket.bind((self.peerserver_ipv4, int(self.peerserver_port)))

        self.peerserver_socket.listen(5)

        while True:
            conn, addr = self.peerserver_socket.accept()
            print 'Connected by', addr

            peer = PeerHandler.PeerHandler(conn, addr, self.fileList)
            peer.start()

        self.peerserver_socket.close()
