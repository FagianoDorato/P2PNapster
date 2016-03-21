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
    session_id = None
    my_ipv4 = "172.030.008.002"
    my_ipv6 = "fc00:0000:0000:0000:0000:0000:0008:0002"
    my_port = "06000"
    dir_ipv4 = "172.030.001.001"
    dir_ipv6 = "fc00:0000:0000:0000:0000:0000:0001:0001"
    dir_ipp2p = dir_ipv4 + dir_ipv6
    dir_port = "03000"
    response_message = None
    files_list = []
    directory = None

    def __init__(self):
        # Searching for shareable files
        for root, dirs, files in os.walk("shareable"):
            for file in files:
                file_md5 = md5.hashfile(open("shareable/" + file, 'rb'), hashlib.md5())
                new_file = SharedFile(file, file_md5)
                self.files_list.append(new_file)

    def login(self):
        print 'Logging in...'
        msg = 'LOGI' + self.my_ipv4 + '|' + self.my_ipv6 + self.my_port
        print 'Login message: ' + msg

        response_message = None
        try:
            self.directory = None
            c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, self.dir_port)
            c.connect()
            self.directory = c.socket
            #self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port)).socket

            self.directory.send(msg)
            print 'Message sent, waiting for response...'
            response_message = self.directory.recv(20)
            print 'Directory responded: ' + response_message
        except socket.error as e:
            print 'Socket Error: ' + e.message
        except Exception as e:
            print 'Error: ' + e.message
        else:
            if response_message is None:
                print 'No response from directory. Login failed'
            else:
                self.session_id = response_message[4:20]
                if self.session_id == '0000000000000000' or self.session_id == '':
                    print 'Troubles with the login procedure.\nPlease, try again.'
                else:
                    print 'Session ID assigned by the directory: ' + self.session_id
                    print 'Login completed'

    def logout(self):
        print 'Logging out...'
        msg = 'LOGO' + self.session_id
        print 'Logout message: ' + msg

        response_message = None
        try:
            # TODO: remove
            #self.directory.close()
            #self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))

            self.directory.send(msg)
            print 'Message sent, waiting for response...'
            response_message = self.directory.recv(7)
            print 'Directory responded: ' + response_message
        except socket.error as e:
            print 'Socket Error: ' + e.message
        except Exception as e:
            print 'Error: ' + e.message
        else:
            if response_message is None:
                print 'No response from directory. Login failed'
            elif response_message[0:4] == 'ALGO':
                self.session_id = None
                number_file = int(response_message[4:7])
                print 'You\'d shared ' + number_file + ' files'
                self.directory.close()
                print 'Logout completed'
            else:
                print 'Error: unknown response from directory.\n'

    def share(self):
        found = False
        while not found:
            print '\nSelect a file to share (\'c\' to cancel):'
            for idx, file in enumerate(self.files_list):
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
                    for idx, file in enumerate(self.files_list):
                        if idx == int_option:
                            found = True
                            print "Adding file " + file.name

                            # TODO: remove
                            #self.directory.close()
                            #self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))

                            msg = 'ADDF' + self.session_id + file.md5 + file.name.ljust(100)
                            print 'Share message: ' + msg

                            response_message = None
                            try:
                                self.directory.send(msg)
                                print 'Message sent, waiting for response...'
                                response_message = self.directory.recv(7)
                                print 'Directory responded: ' + response_message
                            except socket.error as e:
                                print 'Socket Error: ' + e.message
                            except Exception as e:
                                print 'Error: ' + e.message
                            else:
                                if response_message is None:
                                    print 'No response from directory.'
                                else:
                                    print "Copies inside the directory: " + response_message[-3:]

                    if not found:
                        print 'Option not available'
        #   c.close()

    def remove(self):
        found = False
        while not found:
            print "\nSelect a file to remove ('c' to cancel):"
            for idx, file in enumerate(self.files_list):
                print str(idx) + ": " + file.name
            try:
                option = raw_input()
            except SyntaxError:
                option = None
            except Exception:
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
                    for idx, file in enumerate(self.files_list):
                        if idx == int_option:
                            found = True
                            print "Removing file " + file.name

                            # TODO: remove
                            #self.directory.close()
                            #self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))

                            msg = 'DELF' + self.session_id + file.md5
                            print 'Delete message: ' + msg

                            response_message = None
                            try:
                                self.directory.send(msg)
                                print 'Message sent, waiting for response...'
                                response_message = self.directory.recv(7)
                                print 'Directory responded: ' + response_message
                            except socket.error as e:
                                print 'Socket Error: ' + e.message
                            except Exception as e:
                                print 'Error: ' + e.message
                            else:
                                if response_message[-3:] == '999':
                                    print "The file you chose doesn't exist in the directory"
                                else:
                                    print "Copies inside the directory: "+response_message[-3:]

                    if not found:
                            print 'Option not available'

    def search(self):
        print 'Insert search term:'
        try:
            term = raw_input()
        except SyntaxError:
            term = None
        if term is None:
            print 'Please select an option'
        else:
            print "Searching files that match: " + term

            msg = 'FIND' + self.session_id + term.ljust(20)
            print 'Find message: ' + msg
            response_message = None
            try:

                # TODO: remove
                #self.directory.close()
                #self.directory = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.dir_port))

                self.directory.send(msg)
                print 'Message sent, waiting for response...'
                response_message = self.directory.recv(4)
            except socket.error as e:
                print 'Socket Error: ' + e.message
            except Exception as e:
                print 'Error: ' + e.message

            if not response_message == 'AFIN':
                print 'Error: unknown response from directory.\n'
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
                else:
                    try:
                        idmd5 = int(idmd5)
                    except ValueError:
                        print "idmd5 is not a number"
                    else:
                        if idmd5 == 0:
                            print "No results found for search term: " + term
                        elif idmd5 > 0:  # At least one result
                            available_files = []

                            try:
                                for idx in range(0, idmd5):
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
                            else:
                                # visualizza i risultati della ricerca
                                print "Select a file to download ('c' to cancel): "
                                for idx, file in enumerate(available_files):
                                    print str(idx) + ": " + file.name

                                # seleziona un file da scaricare
                                selected_file = None
                                while selected_file is None:
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
                                            selected_file = int(option)
                                        except ValueError:
                                            print "A number is required"

                                file_to_download = available_files[selected_file]

                                # visualizza la lista dei peer da cui è possibile scaricarlo
                                print "Select a peer ('c' to cancel): "
                                for idx, file in enumerate(available_files):
                                    if selected_file == idx:
                                        for idx2, owner in enumerate(file.owners):
                                            print str(idx2) + ": " + owner.ipv4 + " | " + owner.ipv6 + " | " + owner.port

                                selected_peer = None
                                while selected_peer is None:
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
                                            selected_peer = int(option)
                                        except ValueError:
                                            print "A number is required"

                                for idx2, owner in enumerate(file_to_download.owners):
                                    if selected_peer == idx2:
                                        print "Downloading file from: " + owner.ipv4 + " | " + owner.ipv6 + " " + owner.port
                                        Download.get_file(self.session_id, owner.ipv4, owner.ipv6, owner.port, file_to_download, self.directory)
                                        #Download.warns_directory(self.session_id, file_to_download.md5, )
                        else:
                            print "Unknown error, check your code!"
