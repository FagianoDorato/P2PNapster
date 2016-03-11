import socket
import json
import SharedFile
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
  cmd = conn.recv(4)

  if not cmd: break
  print "received command: " + str(cmd)
  sessionId = conn.recv(16)
  print "received sessionID: " + str(sessionId)
  term = conn.recv(20)
  print "received search term: " + str(term)

  idmd5 = str(3).zfill(3)
  response = bytes('AFIN', "utf-8") + bytes(idmd5, "utf-8")
  conn.send(response)

conn.close()