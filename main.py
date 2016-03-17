import os
from modules import Peer
from modules import ServerSocket
import threading
from multiprocessing import Process
from modules import PeerServer
# main
p = Peer.Peer()

while p.sessionId is None:
    print 'Select one of the following options:'
    print '1: Log In'
    int_option = None
    while int_option is None:
        try:
            option = raw_input()
        except SyntaxError:
            option = None

        if option is None:
            print 'Please select an option'
        else:
            try:
                int_option = int(option)
            except ValueError:
                print "A number is required"

    if int_option != 1:
        print 'Option ' + str(option) + ' not available'
    else:
        p.login()

        # TODO: Start peer server
        peerserver = PeerServer.PeerServer(p.my_ipv4, p.my_ipv6, p.my_port, p.filesList)
        peerserver.start()

        while p.sessionId is not None:
            print "\nSelect one of the following options:"
            print "1: Add File"
            print "2: Remove File"
            print "3: Search File"
            print "4: LogOut"

            int_option = None
            while int_option is None:
                try:
                    option = raw_input()
                except SyntaxError:
                    option = None

                if option is None:
                    print 'Please select an option'
                else:
                    try:
                        int_option = int(option)
                    except ValueError:
                        print "A number is required"

            if int_option == 1:
                p.share()
            elif int_option == 2:
                p.remove()
            elif int_option == 3:
                p.search()
            elif int_option == 4:
                p.logout()
                # TODO: stop peer server
                #peerserver.stop()
            else:
                print 'Option ' + str(int_option) + ' not available'
