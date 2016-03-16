#   socket.inet_aton('172.0.0.1') mi trasforma una stringa ipv4 in un ipv4 per il sistema
#   socket.inet_pton(socket.AF_INET6, some_string)
import socket
import os
import sys
import random
from thread import *

class Connection:
    #   SessionID = None
    socketDirectory = None
    socketPeer = None
    dir_ipv4 = None
    dir_port = None
    dir_ipv6 = None
    ip_selector = random.randrange(0, 100) % 2
    string_read = None
    size = 1024
    message_received = None

    #   ip: string ipv6 + ipv4
    def __init__(self, ipv4, ipv6, port):
        self.dir_ipv4 = ipv4
        self.dir_ipv6 = ipv6
        self.dir_port = port
        #self.ipv4 = '127.0.0.1'
        #self.ipv6 = '::1'
        #print (self.dir_ipv4)
        #print (self.dir_ipv6)
        if self.ip_selector == 0:
            self.ip_selector = 1
            self.socketDirectory = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socketDirectory.connect((self.dir_ipv4, self.dir_port))
                #print ("\t--->Succesfully connected ipv4!\n")
            except socket.error, msg:
                print ("--!!!--> Connection error ipv4! <--!!!--\nTerminated.\nSocket.error : %s" % msg)
                print self.dir_ipv4 + str(self.dir_port)

        else:  # case: ipv6
            self.ip_selector = 0
            self.socketDirectory = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            try:
                self.socketDirectory.connect((self.dir_ipv6, self.dir_port))
                #print ("\t--->Succesfully connected ipv6!\n")
            except socket.error, msg:
                print ("--!!!--> Connection error ipv6! <--!!!--\nTerminated.\nSocket.error : %s" % msg)
                print self.dir_ipv4 + str(self.dir_port)

