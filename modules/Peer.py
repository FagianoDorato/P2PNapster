# coding=utf-8
import os
from SharedFile import SharedFile
from Owner import Owner
import Download
import hashlib
import socket
import Connection
import base64

dirIP = '127.0.0.1'
dir_port = 3000

# Helper Methods
def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()


def fileExists(list, md5):
    for l in list:
        if l.md5.lower() == md5.lower():
            return True


class Peer(object):
    sessionId = None
    my_ipv4 = "172.030.008.002"
    my_ipv6 = "fc00:0000:0000:0000:0000:0000:0008:0002"
    my_port = "06500"
    dir_ipv4 = "172.030.008.005"
    dir_ipv6 = "fc00:0000:0000:0000:0000:0000:0008:0005"
    dir_ipp2p = dir_ipv4 + dir_ipv6
    dir_port = "03000"
    response_message = None
    filesList = []
    number_share_files = 0


    def __init__(self):
        # Searching for shareable files
        for root, dirs, files in os.walk("shareable"):
            for file in files:
                fileMd5 = hashfile(open("shareable/" + file, 'rb'), hashlib.md5())
                newFile = SharedFile(file, fileMd5)
                self.filesList.append(newFile)

    def login(self):
        # TODO: Log in and return sessionId
        msg = ('LOGI' + self.my_ipv4 + '|' + self.my_ipv4 + self.my_port)
        print('messaaggio login: ' + msg)
        c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.port))
        c.socketDirectory.send(msg)
        response_message = c.socketDirectory.recv(20)
        self.sessionId = response_message[4:20]
        if self.sessionId == '0000000000000000' or self.sessionId == '':
            print "problems with the login.\nPlease, try again."
        else:
            print "sessionID assigned by the directory: " + self.sessionId

        c.socketDirectory.close()

    def logout(self):
        # TODO: Log out
        msg = 'LOGO' + self.sessionId
        print "message logout: " + msg
        c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.port))
        c.socketDirectory.send(msg)
        cmd = c.socketDirectory.recv(4)
        if not cmd:
            print "error"
        if cmd == "ALGO":
            self.sessionId = None
        #number_file = int(response_message[4:7])
        #if number_file != self.number_share_files:
        #    print "error number delete file"
        #self.sessionId = None
        #print "Logout completed"
        c.socketDirectory.close()

    def share(self):
        print "Select a file to share"
        for idx, file in enumerate(self.filesList):
            print str(idx) + ": " + file.name
        option = input()

        for idx, file in enumerate(self.filesList):
            if idx == int(option):
                print "Adding file " + file.name
                # TODO: add file
                c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.port))
                formatSend = 'ADDF' + self.sessionId + file.md5 + file.name.ljust(100)
                c.socketDirectory.send(formatSend)

                print formatSend
                response=c.socketDirectory.recv(7)
                print response
                print "after insert.."
                print "files inside the directory: "+response[-3:]
                print "done"

        c.socketDirectory.close()

    def remove(self):
        print "Select a file to remove"
        for idx, file in enumerate(self.filesList):
            print str(idx) + ": " + file.name
        option = input()

        for idx, file in enumerate(self.filesList):
            if idx == int(option):
                print "Removing file " + file.name
                # TODO: remove file
                c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.port))
                formatSend = 'DELF' + self.sessionId + file.md5
                c.socketDirectory.send(formatSend)

                print formatSend
                response = c.socketDirectory.recv(7)
                print response

                if response[-3:] == '999':
                    print "file not exist in a directory"
                else:
                    print "after removing.."
                    print "files inside the directory: "+response[-3:]
                    print "done"

    def search(self):
        print "Insert search term:"
        term = raw_input()
        print "Searching files that match: " + term
        # TODO: search files
        c = Connection.Connection(self.dir_ipv4, self.dir_ipv6, int(self.port))
        cmd = 'FIND' + self.sessionId + term.ljust(20)
        c.socketDirectory.send(cmd)

        r = c.socketDirectory.recv(4)
        if not r == 'AFIN':
            print "Error"
        else:
            idmd5 = c.socketDirectory.recv(3)
            if idmd5 != 0:  # At least one result
                availableFiles = []

                for idx in range(0, int(idmd5)):
                    file_i_md5 = c.socketDirectory.recv(16)
                    file_i_name = c.socketDirectoryrecv(100).strip()
                    file_i_copies = c.socketDirectoryrecv(3)
                    file_owners = []
                    for copy in range(0, int(file_i_copies)):
                        owner_j_ipv4 = c.socketDirectory.recv(16).replace("|", "")  # ipv4
                        owner_j_ipv6 = c.socketDirectoryrecv(39)  # ipv6
                        owner_j_port = c.socketDirectory.recv(5)  # port
                        file_owners.append(Owner(owner_j_ipv4, owner_j_ipv6, owner_j_port))

                    availableFiles.append(SharedFile(file_i_name, file_i_md5, file_owners))

                print "Files matching the search term: "
                for file in availableFiles:
                    print "\n\nname: " + file.name
                    print "md5: " + base64.encodestring(file.md5)

                    for idx, owner in enumerate(file.owners):
                        print "Owner " + str(idx)
                        print "ipv4: " + str(owner.ipv4)
                        print "ipv6: " + str(owner.ipv6)
                        print "port: " + str(owner.port)

                self.download(availableFiles)

            elif idmd5 == 0:
                print "No results found for search term: " + term
            else:
                print "Unknown error, check your code!"
    # self.download(availableFiles)

    #  availableFiles è una lista recuperata tramite la ricerca che contiene i risultati
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
                for idx2, owner in file.owners:
                    print str(idx2) + ": " + owner.ipv4 + " | " + owner.ipv6 + " | " + owner.port

            option = input()
            for idx2, owner in file.owners:
                if option == idx2:
                    print "Downloading file..."
                    Download.get_file(owner.ipv4, owner.ipv6, owner.port, file)
                    Download.warns_directory(self.sessionId, file.md5)
