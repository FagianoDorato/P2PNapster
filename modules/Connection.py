#   socket.inet_aton('172.0.0.1') mi trasforma una stringa ipv4 in un ipv4 per il sistema
#   socket.inet_pton(socket.AF_INET6, some_string)
import socket
import os
import sys
import random
from thread import *


class Connection:
    #   SessionID = None
    socket = None
    ipv4 = None
    port = None
    ipv6 = None
    string_read = None
    message_received = None

    #   ip: string ipv6 + ipv4
    def __init__(self, ipv4, ipv6, port):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port
        #self.ipv4 = '127.0.0.1'
        #self.ipv6 = '::1'
        #print (self.dir_ipv4)
        #print (self.dir_ipv6)

    def connect(self):
        if random.choice([0, 1]) == 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.ipv4, self.port))
                print ("Succesfully connected to :" + self.ipv4 + str(self.port))
            except socket.error, msg:
                print ("Connection error ipv4!\nTerminated.\nSocket.error : %s" % msg)
                print self.ipv4 + str(self.port)

        else:
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.ipv6, self.port))
                print ("Succesfully connected to :" + self.ipv6 + str(self.port))
            except socket.error, msg:
                print ("Connection error ipv6!\nTerminated.\nSocket.error : %s" % msg)
                print self.ipv4 + str(self.port)

    def listen(self):
        if random.choice([0, 1]) == 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                self.socket.bind((self.ipv4, self.port))
                self.socket.listen(5)
                print ("Succesfully connected to :" + self.ipv4 + str(self.port))
            except socket.error, msg:
                print ("Connection error ipv4!\nTerminated.\nSocket.error : %s" % msg)
                print self.ipv4 + str(self.port)

        else:
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                self.socket.bind((self.ipv6, self.port))
                self.socket.listen(5)
                print ("Succesfully connected to :" + self.ipv6 + str(self.port))
            except socket.error, msg:
                print ("Connection error ipv6!\nTerminated.\nSocket.error : %s" % msg)
                print self.ipv4 + str(self.port)