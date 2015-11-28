#!/usr/bin/env python

import socket
import Queue


def receiveTCP(q_send,q_rec):

    #initializ the receive queue
    q_rec.put(0)

    TCP_IP = raw_input('Enter IPv4 of this Machine: ')

    #port this machine listens on
    #this needs to be the send port of other machine
    #
    TCP_PORT = 8888
    BUFFER_SIZE = 1024

    #create a tuple with port and ip
    DEST = (TCP_IP, TCP_PORT)


    #begin process of accepting incoming connection on designated port
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((DEST))
    s.listen(1)
    conn, addr = s.accept()

    #prints who we are connected to
    #
    print 'Connection address:', addr

    #wait for messages
    while 1:

        #first we check if the send queue is empty
        if q_send.empty():
            #if the send q is empty, put a 0 on it.
            q_send.put(0)

        #check what is on the send queue.  If it is 1, break from the
        #while loop which terminates the thread. We also have to close the socket
        check = q_send.get()
        if check:
            conn.close()
            break

        data = conn.recv(BUFFER_SIZE)
        print "received data:", data
        
        #if we received EXIT from the other machine, signal the
        #sending thread to terminate and break from the while loop
        #which closes the program
        #
        if data == 'EXIT':
            conn.close()
            s.close()
            q_rec.put(1)
            break
        else:
            q_rec.put(0)


    #conn.send(data)  # echo
    print "closing send thread"
