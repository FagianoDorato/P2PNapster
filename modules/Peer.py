# coding=utf-8
import os
from SharedFile import SharedFile
from Owner import Owner
import Download
import hashlib
import socket
import Connection
import md5

class Peer(object):
    sessionId = None
    my_ipv4 = "172.030.008.002"
    my_ipv6 = "fc00:0000:0000:0000:0000:0000:0008:0002"
    my_port = "06000"
    dir_ipv4 = "172.030.008.004"
    dir_ipv6 = "fc00:0000:0000:0000:0000:0000:0008:0004"
    dir_ipp2p = dir_ipv4 + dir_ipv6
    dir_port = "03000"
    response_message = None
    filesList = []
    number_share_files = 0
    directory = None

    def __init__(self):
        # Searching for shareable files
        for root, dirs, files in os.walk("shareable"):
            for file in files:
                file_md5 = md5.hashfile(open("shareable/" + file, 'rb'), hashlib.md5())
                new_file = SharedFile(file, file_md5)
                self.filesList.append(new_file)

    def login(self):
        print 'Logging in...'
        msg = ('LOGI' + self.my_ipv4 + '|' + self.my_ipv6 + self.my_port)
        print 'Login message: ' + msg

        response_message = None
        try:
            self.directory = None
            self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port)).socketDirectory
            self.directory.send(msg)
            print 'Message sent, waiting for response...'
            response_message = self.directory.recv(20)
        except Exception as e:
            print 'Error: ' + e.message

        if response_message is None:
            print "Login failed."
        else:
            self.sessionId = response_message[4:20]
            if self.sessionId == '0000000000000000' or self.sessionId == '':
                print "problems with the login.\nPlease, try again."
            else:
                print "sessionID assigned by the directory: " + self.sessionId
        #c.close()

    def logout(self):
        print 'Logging out...'
        msg = 'LOGO' + self.sessionId
        print "Logout message: " + msg

        response_message = None
        try:
            # TODO: remove
            self.directory.close()
            self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))
            self.directory.send(msg)
            print 'Message sent, waiting for response...'
            response_message = self.directory.recv(7)
        except Exception as e:
            print 'Error: ' + e.message

        if response_message is None:
            print "Login failed."
        elif response_message[0:3] == 'ALGO':
            self.sessionId = None
            number_file = int(response_message[4:7])
            print "You'd shared " + number_file + "files"
            self.directory.close()
            print "Logout completed"

    def share(self):
        found = False
        while not found:
            print "\nSelect a file to share ('c' to cancel):"
            for idx, file in enumerate(self.filesList):
                print str(idx) + ": " + file.name

            try:
                option = raw_input()
            except SyntaxError:
                option = None

            if option is None:
                print 'Please select an option'
            elif option == "c":
                break
            else:
                try:
                    int_option = int(option)
                except ValueError:
                    print "A number is required"
                else:
                    for idx, file in enumerate(self.filesList):
                        if idx == int_option:
                            found = True
                            print "Adding file " + file.name

                            # TODO: remove
                            self.directory.close()
                            self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))


                            msg = 'ADDF' + self.sessionId + file.md5 + file.name.ljust(100)
                            print 'Share message: ' + msg

                            try:
                                self.directory.send(msg)
                                response = self.directory.recv(7)
                                print "Copies inside the directory: "+response[-3:]
                            except socket.error as e:
                                print 'Socket Error: ' + e.message
                            except Exception as e:
                                print 'Error: ' + e.message

                    if not found:
                        print 'Option not available'
        #   c.close()

    def remove(self):
        found = False
        exit = False
        while not found and not exit:
            print "\nSelect a file to remove ('c' to cancel):"
            for idx, file in enumerate(self.filesList):
                print str(idx) + ": " + file.name
            try:
                option = raw_input()
            except SyntaxError:
                option = None

            if option is None:
                print 'Please select an option'
            elif option == "c":
                break
            else:
                try:
                    int_option = int(option)
                except ValueError:
                    print "A number is required"
                else:
                    for idx, file in enumerate(self.filesList):
                        if idx == int_option:
                            found = True
                            print "Removing file " + file.name


                            # TODO: remove
                            self.directory.close()
                            self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))


                            msg = 'DELF' + self.sessionId + file.md5
                            print 'Delete message: ' + msg

                            try:
                                self.directory.send(msg)
                                response = self.directory.recv(7)
                                if response[-3:] == '999':
                                    print "doesn't exist in the directory"
                                else:
                                    print "Copies inside the directory: "+response[-3:]
                            except socket.error as e:
                                print 'Socket Error: ' + e.message
                            except Exception as e:
                                print 'Error: ' + e.message

                    if not found:
                            print 'Option not available'

    def search(self):
        print "Insert search term:"
        try:
            term = raw_input()
        except SyntaxError:
            term = None
        if term is None:
            print 'Please select an option'
        else:
            print "Searching files that match: " + term

            cmd = 'FIND' + self.sessionId + term.ljust(20)

            try:

                # TODO: remove
                self.directory.close()
                self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))
                self.directory.send(cmd)

                r = self.directory.recv(4)
            except socket.error as e:
                print 'Socket Error: ' + e.message
            except Exception as e:
                print 'Error: ' + e.message

            if not r == 'AFIN':
                print "Error AFIN", r
            else:
                idmd5 = None
                try:
                    idmd5 = self.directory.recv(3)
                except socket.error as e:
                    print 'Socket Error: ' + e.message
                except Exception as e:
                    print 'Error: ' + e.message

                if idmd5 is None:
                    print 'Error: idmd5 is blank'
                    return

                try:
                    idmd5 = int(idmd5)
                except ValueError:
                    print "idmd5 is not a number"
                else:
                    if idmd5 == 0:
                        print "No results found for search term: " + term
                        return
                    elif idmd5 > 0:  # At least one result
                        available_files = []

                        try:
                            for idx in range(0, int(idmd5)):
                                file_i_md5 = self.directory.recv(32)
                                file_i_name = self.directory.recv(100).strip()
                                file_i_copies = self.directory.recv(3)
                                file_owners = []
                                for copy in range(0, int(file_i_copies)):
                                    owner_j_ipv4 = self.directory.recv(16).replace("|", "")  # ipv4
                                    owner_j_ipv6 = self.directory.recv(39)  # ipv6
                                    owner_j_port = self.directory.recv(5)  # port
                                    file_owners.append(Owner(owner_j_ipv4, owner_j_ipv6, owner_j_port))

                                available_files.append(SharedFile(file_i_name, file_i_md5, file_owners))

                        except socket.error as e:
                            print 'Socket Error: ' + e.message
                        except Exception as e:
                            print 'Error: ' + e.message

                        if len(available_files) == 0:
                            print "No results found for search term: " + term
                            return

                        # visualizza i risultati della ricerca
                        print "Select a file to download ('c' to cancel): "
                        for idx, file in enumerate(available_files):
                            print str(idx) + ": " + file.name

                        # seleziona un file da scaricare
                        int_option = None
                        while int_option is None:
                            try:
                                option = raw_input()
                            except SyntaxError:
                                option = None

                            if option is None:
                                print 'Please select an option'
                            elif option == 'c':
                                return
                            else:
                                try:
                                    int_option = int(option)
                                except ValueError:
                                    print "A number is required"


                        # visualizza la lista dei peer da cui è possibile scaricarlo
                        print "Select a peer ('c' to cancel): "
                        for idx, file in enumerate(available_files):
                            if int_option == idx:
                                for idx2, owner in enumerate(file.owners):
                                    print str(idx2) + ": " + owner.ipv4 + " | " + owner.ipv6 + " | " + owner.port

                        int_option = None
                        while int_option is None:
                            try:
                                option = raw_input()
                            except SyntaxError:
                                option = None

                            if option is None:
                                print 'Please select an option'
                            elif option == 'c':
                                return
                            else:
                                try:
                                    int_option = int(option)
                                except ValueError:
                                    print "A number is required"

                        for idx2, owner in enumerate(file.owners):
                            if int_option == idx2:
                                print "Downloading file from: " + owner.ipv4 + " | " + owner.ipv6 + " " + owner.port
                                Download.get_file(owner.ipv4, owner.ipv6, owner.port, file)
                                Download.warns_directory(self.sessionId, file.md5, self.directory.socketDirectory)
                    else:
                        print "Unknown error, check your code!"


            #c.close()
        # self.download(availableFiles)


    '''#  availableFiles è una lista recuperata tramite la ricerca che contiene i risultati
    def download(self, availableFiles):
        # visualizza i risultati della ricerca
        print "Select a file to download: "
        for idx, file in enumerate(availableFiles):
            print str(idx) + ": " + file.name
        # seleziona un file da scaricare
        option = input()

        # visualizza la lista dei peer da cui è possibile scaricarlo
        print "Select a peer: "
        for idx, file in enumerate(availableFiles):
            if option == idx:
                for idx2, owner in enumerate(file.owners):
                    print str(idx2) + ": " + owner.ipv4 + " | " + owner.ipv6 + " | " + owner.port

        option = input()
        for idx2, owner in enumerate(file.owners):
            if option == idx2:
                print "Downloading file from: " + owner.ipv4 + " | " + owner.ipv6 + " " + owner.port
                Download.get_file(owner.ipv4, owner.ipv6, owner.port, file)
                #c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))
                #Download.warns_directory(self.sessionId, file.md5, c)
        
        c.close()'''