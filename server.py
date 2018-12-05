# responsável por gerenciar os pontos
# responsável por armazenar e notificar os observadores

# import threading
# import socket
# from point import Point

# class Server:
#   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   subscribers = []
#   host = '127.0.0.1'
#   port = 5000

#   def __init__(self):
#     print('server initialized')
#     self.sock.bind((self.host, self.port))
#     self.sock.listen(1)

#     t = threading.Thread(target=self.sendMsg)
#     t.daemon = True
#     t.start()

#   def notifyAll(self, message):
#     for subscriber in self.subscribers:
#       subscriber.send(message.encode('utf8'))

#   def sendMsg(self):
#     while True:
#       message = input('-> ')
#       self.notifyAll(message)

#   def handler(self, c, a):
#     while True:
#       data = c.recv(1024)
#       if not data:
#         print(str(a[0]) + ':' + str(a[1]), 'disconnected')
#         self.subscribers.remove(c)

#   def run(self):
#     while True:
#       c, a = self.sock.accept()
#       self.subscribers.append(c)
#       print(str(a[0]) + ':' + str(a[1]), 'connected')

# s = Server()
# s.run()

import socket
import threading
from message import Message
import pickle
import sys
import uuid
import numpy as np
import matplotlib._color_data as mcd
import random
from point import Point
import time

class Server:
  host = '127.0.0.1'
  port = 5000
  observers = []
  servers = []
  isMaster = False
  sock = socket.socket()
  # master = []
  id = -1

  def __init__(self, port, masterHost, masterPort):
    self.port = port
    self.id = str(uuid.uuid1()) # based on ip and time
    if masterHost and masterPort:
      self.servers.append((masterHost, masterPort, ''))
      self.isMaster = False
    else:
      self.servers.append((self.host, self.port, self.id))
      self.isMaster = True

  def notifyAll(self, message):
    for connection in self.observers:
      connection.send(message.encode())

  def handler(self, c, a):
    while True:
      data = c.recv(1024)
      if not data:
        print('not data')
        self.observers.remove(c)
        c.close()
        break
      received = pickle.loads(data)
      print(received, '({} bytes)'.format(len(data)))
      if received.header == 'registerServer':
        self.servers.append(received.body)
        self.notifyAll(Message('updateServers', self.servers))
      # for connection in self.observers:
        # message = Message('message', data.decode('utf8'))
        # encoded = pickle.dumps(message)
        # connection.send(encoded)

  def generatePoint(self):
    x = np.random.random()*10
    y = np.random.random()*10
    c = list(mcd.CSS4_COLORS.keys())[random.randrange(len(mcd.CSS4_COLORS.keys()))]
    return Point(x, y, c)

  def generateFrame(self):
    input('press any key to start to generate frames')
    maxPoints = 10
    while True:
      points = []
      while len(points) < maxPoints:
        points.append(self.generatePoint())
        print('point generated')
        time.sleep(1)
      print('send frame')
      self.notifyAll(Message('newFrame', points))

  def run(self):
    if (not self.isMaster): # listen to MASTER updates
      print(self.servers)
      while len(self.servers) > 0 and self.servers[0][2] != self.id:
        sock = socket.socket()
        sock.connect((self.servers[0][0], self.servers[0][1]))

        while True:
          data = sock.recv(1024)
          if not data:
            print('server disconnected')
            break
          received = pickle.loads(data)
          print(received, '({} bytes)'.format(len(data)))
          if received.header == 'greeting':
            sock.send(Message('registerServer', (self.host, self.port, self.id)).encode())
          elif received.header == 'updateServers':
            self.servers = received.body
            print(self.servers)
        self.servers.pop(0)

    # start master work
    fThread = threading.Thread(target=self.generateFrame)
    fThread.daemon = True
    fThread.start()

    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    print('listening on {}:{}'.format(self.host, self.port))
    self.sock.listen(1)

    while True:
      c,a = self.sock.accept()
      cThread = threading.Thread(target=self.handler, args=(c, a))
      cThread.daemon = True
      cThread.start()
      self.observers.append(c)
      # c.send(pickle.dumps(Message('greeting', 'Hello')))
      c.send(Message('greeting', 'Hello').encode())
      print(str(a[0]) + ':' + str(a[1]), 'connected')
      print(self.observers)

def main(argv):
  master = (None, None)
  if (len(argv) == 3):
    master = (argv[1], int(argv[2]))
  server = Server(int(argv[0]), master[0], master[1])
  server.run()

if __name__ == '__main__':
  main(sys.argv[1:])
