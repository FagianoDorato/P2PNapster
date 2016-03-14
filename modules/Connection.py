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
    ipv4 = None
    port = None
    ipv6 = None
    boolean = random.randrange(0, 100) % 2
    string_read = None
    size = 1024
    message_received = None

    #   ip: string ipv6 + ipv4
    def __init__(self, ipv4, ipv6, port):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.port = port
        self.ipv4 = '127.0.0.1'
        self.ipv6 = '::1'
        print (self.ipv4)
        print (self.ipv6)
        if self.boolean:
            self.socketDirectory = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socketDirectory.connect((self.ipv4, self.port))
                print ("\t--->Succesfully connected ipv4!\n")
            except socket.error, msg:
                print ("--!!!--> Connection error ipv4! <--!!!--\nTerminated.\nSocket.error : %s" % msg)
        #   case: ipv6
        else:
            self.socketDirectory = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            try:
                self.socketDirectory.connect((self.ipv6, self.port))
                print ("\t--->Succesfully connected ipv6!\n")
            except socket.error, msg:
                print ("--!!!--> Connection error ipv6! <--!!!--\nTerminated.\nSocket.error : %s" % msg)



    # #   message_sent: message to be sent
    # def send(self, message_sent):
    #     #   case: ipv4
    #     if self.boolean:
    #         self.socketDirectory = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         try:
    #             self.socketDirectory.connect((self.ipv4, self.pp2p))
    #             print ("\t--->Succesfully connected ipv4!\n")
    #         except:
    #             print ("--!!!--> Connection error ipv4! <--!!!--\nTerminated.")
    #         while True:
    #             self.socketDirectory.send(message_sent)
    #             string_read = self.socketDirectory.recv(1024)
    #         if not string_read:
    #             return '000000'
    #         self.boolean = False
    #         self.socketDirectory.close()
    #         return string_read[5:17]
    #     #   case: ipv6
    #     else:
    #         self.socketDirectory = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    #         try:
    #             self.socketDirectory.bind((self.ipv6, self.pp2p))
    #             print ("\t--->Succesfully connected ipv6!\n")
    #         except:
    #             print ("--!!!--> Connection error ipv6! <--!!!--\nTerminated.")
    #         while True:
    #             self.socketDirectory.send(message_sent)
    #             string_read = self.socketDirectory.recv(1024)
    #             if not string_read:
    #                 return '000000'
    #             self.boolean = True
    #             self.socketDirectory.close()
    #             return string_read

    #   server
    def start_server(lista_file):
        #creo un nuvo processo in ascolto delle richieste dei peer
        newpid = os.fork()
        if newpid == 0:              #sono nel processo figlio
            HOST = None               # Symbolic name meaning all available interfaces
            PORT = 3000              # Arbitrary non-privileged port
            s = None
            for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                af, socktype, proto, canonname, sa = res
                try:
                    s = socket.socket(af, socktype, proto)
                except socket.error as msg:
                    s = None
                    continue
                try:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(sa)
                    s.listen(5)
                except socket.error as msg:
                    s.close()
                    s = None
                    continue
                break
            if s is None:
                print 'could not open socket'
                sys.exit(1)

            while True:
                #wait to accept a connection - blocking call
                conn, addr = s.accept()
                print 'Connected by', addr

                #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
                #start_new_thread(clientthread ,(conn, lista_file))
            s.close()
        else:
            return "Server inizializzato!"

    #   server by Zotti
    @staticmethod
    def server(self):
        size = 20
        print("start server")
        socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((self.ipv4, self.pp2p))
        socket_server.listen(5)
        while 1:
            print("Attesa connessione peer")
            client, address = socket_server.accept()
            new_pid = os.fork()
            if new_pid == 0:
                try:
                    socket_server.close()
                    while 1:
                        stringa_ricevuta = client.recv(size)
                        if stringa_ricevuta== "":
                            print("\t\tempty socket")
                            break
                        operazione = stringa_ricevuta[0:4]
                        #   send msg
                        if operazione.upper() == "RETR":
                            md5 = stringa_ricevuta[4:20]
                            print ("\t\tdownload request from a peer, md5: %s" % md5)
                            client.send("ARET" + "non so cosa scrivere")
                except Exception as e:
                    print e
                    print("Errore ricezione")
                finally:
                    client.close()
            else:
                client.close()

        print("Terminato server")


    #   method for receiving download request from the Peer by zotti
    # def accept(self):
    #     if self.boolean:
    #         self.socketPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         try:
    #             self.socketPeer.bind((self.ipv4, self.pp2p))
    #             print ("\t--->Succesfully bind ipv4!\n")
    #         except:
    #             print ("--!!!--> Connection error ipv4! <--!!!--\nTerminated.")
    #         self.socketPeer.listen(1)
    #         client, addr = self.socketPeer.accept()
    #         print 'Connection address:', addr
    #         while True:
    #             self.message_received = client.recv(self.size)
    #             if self.message_received == "":
    #                 print("\t\tsocket vuota")
    #                 break
    #             client.close()
    #             return self.message_received


    # def __init__(self):
    #     if self.boolean:
    #         self.socketDirectory = SocketOpen.SocketOpen(self.ipv4, 3000)
    #         self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.socketDirectory.ConnectIP6()
    #         self.boolean = False
    #     else:
    #         self.socketDirectory = SocketOpen.SocketOpen(self.ipv6, 3000)
    #         self.socketDirectory.ConnectIP4()
    #         self.boolean = True
    #     self.ipp2p = self.ipv6 + self.ipv4
    #
    # @classmethod
    # def login(cls):
    #     #   open socket connection with directory
    #     if cls.boolean:
    #         cls.socketDirectory = SocketOpen.SocketOpen(cls.ipv4, 3000)
    #         cls.socketDirectory.ConnectIP6()
    #         cls.boolean = False
    #     else:
    #         cls.socketDirectory = SocketOpen.SocketOpen(cls.ipv6, 3000)
    #         cls.socketDirectory.ConnectIP4()
    #         cls.boolean = True
    #     cls.ipp2p = cls.ipv6 + cls.ipv4
    #     #   send the msg
    #     msg = ('LOGI' + cls.ipp2p + cls.pp2p)
    #     cls.socketDirectory.send(msg)
    #     cls.socketDirectory.liste(10)
    #     client, address = cls.socketDirectory.accept()
    #     string_read = client.recv(1024)
    #     if string_read == '' or string_read[0:4] != 'ALGI':
    #         print("\t\tsocket vuota o errata")
    #         #   break
    #     return string_read[0:4]
    #
    # @classmethod
    # def logout(cls):
    #     msg = ('LOGI' + cls.ipp2p + cls.pp2p)
    #     cls.socketDirectory.send(msg)
    #     while 1:
    #         cls.socketDirectory = None
    #     cls.socketDirectory.close()
    #
    # @staticmethod
    # def connect_directory(self):
    #     if self.boolean:
    #         self.socketDirectory = SocketOpen.SocketOpen(self.ipv4, 3000)
    #         self.socketDirectory.ConnectIP6()
    #         self.boolean = False
    #     else:
    #         self.socketDirectory = SocketOpen.SocketOpen(self.ipv6, 3000)
    #         self.socketDirectory.ConnectIP4()
    #         self.boolean = True
    #     #self.ipp2p = self.ipv6 + self.ipv4
    #     return self.socketDirectory
    #
    # def disconnect(self):
    #     self.socketDirectory.close()
    #
