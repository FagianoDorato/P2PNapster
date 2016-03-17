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
    try:
        option = input()
    except SyntaxError:
        option = None

    if option is None:
        print 'Please select an option'
    elif option != 1:
        print 'Option ' + str(option) + ' not available'
    else:
        p.login()

        # TODO: Start peer server
        #peerserver = PeerServer.PeerServer(p.my_ipv4, p.my_ipv6, p.my_port, p.filesList)
        #peerserver.start()

        while p.sessionId is not None:
            print "\nSelect one of the following options:"
            print "1: Add File"
            print "2: Remove File"
            print "3: Search File"
            print "4: LogOut"

            try:
                option = input()
            except SyntaxError:
                option = None

            if option is None:
                print 'Please select an option'
            else:
                if option == 1:
                    p.share()
                elif option == 2:
                    p.remove()
                elif option == 3:
                    p.search()
                elif option == 4:
                    p.logout()
                    # TODO: stop peer server
                    #peerserver.stop()
                else:
                    print 'Option ' + str(option) + ' not available'
