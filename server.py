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

class Server:
  host = '127.0.0.1'
  port = 5000
  observers = []
  master = False
  sock = socket.socket()

  def __init__(self, host, port, isMaster=False):
    self.host = host
    self.port = port
    self.master = isMaster

  def handler (self, c, a):
    while True:
      data = c.recv(1024)
      if not data:
        print('not data')
        self.observers.remove(c)
        c.close()
        break
      for connection in self.observers:
        message = Message('message', data.decode('utf8'))
        encoded = pickle.dumps(message)
        connection.send(encoded)

  def run(self):
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(1)

    while True:
      c, a = self.sock.accept()
      cThread = threading.Thread(target=self.handler, args=(c, a))
      cThread.daemon = True
      cThread.start()
      self.observers.append(c)
      # c.send(pickle.dumps(Message('greeting', 'Hello')))
      c.send(Message('greeting', 'Hello').encode())
      print(str(a[0]) + ':' + str(a[1]), 'connected')
      print(self.observers)

def main(argv):
  server = Server(argv[0], int(argv[1]))
  if (len(argv) == 3):
    server.master = bool(argv[2])
  server.run()

if __name__ == '__main__':
  main(sys.argv[1:])
