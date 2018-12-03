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

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 5000
connections = []

sock.bind((host, port))
sock.listen(1)

def handler (c, a):
  global connections
  while True:
    data = c.recv(1024)
    if not data:
      print('not data')
      connections.remove(c)
      c.close()
      break
    for connection in connections:
      message = Message('message', data.decode('utf8'))
      encoded = pickle.dumps(message)
      connection.send(encoded)

while True:
  c, a = sock.accept()
  cThread = threading.Thread(target=handler, args=(c, a))
  cThread.daemon = True
  cThread.start()
  connections.append(c)
  print(str(a[0]) + ':' + str(a[1]), 'connected')
  print(connections)
