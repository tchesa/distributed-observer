# responsável por receber as notificações do servidor
# responsável por armazenar e plotar os pontos recebidos

# import numpy as np
# import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 10])

# for i in range(1000):
#   x = np.random.random()*10
#   y = np.random.random()*10
#   plt.scatter(x, y)
#   plt.pause(0.05)

# plt.show()

# import socket
# import threading

# class Client:
#   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   server = ('127.0.0.1', 5000)
#   shutdown = False

#   def sendMsg(self):
#     while not self.shutdown:
#       self.shutdown = input('exit (y/n)? ') == "y"
#     # self.sock.close()

#   def __init__(self, address):
#     self.sock.connect(self.server)

#     t = threading.Thread(target=self.sendMsg)
#     t.daemon = True
#     t.start()

#     while not self.shutdown:
#       try:
#         data = self.sock.recv(1024)
#         if not data:
#           break
#         print(data.decode('utf8'))
#       except:
#         print('error')

# client = Client('127.0.0.1')

import socket
import threading
import pickle
from message import Message
from point import Point
import sys
import uuid
import numpy as np
import matplotlib.pyplot as plt

class Client:
  host = '127.0.0.1'
  port = 5000
  sock = socket.socket()
  points = []

  def __init__(self, host, port):
    self.host = host
    self.port = port

  def send(self, sock):
    message = input(': ')
    while True:
      self.sock.send(message.encode('utf8'))
      message = input(': ')

  def render(self):
    plt.axis([0, 10, 0, 10])
    plt.show()
    print('shown')
    while True:
      for point in self.points:
        plt.scatter(point.x, point.y, c=point.c)
      plt.pause(0.05)
      plt.clf()

  def run(self):
    self.sock.connect((self.host, self.port))

    sThread = threading.Thread(target=self.send, args=(self.sock,))
    sThread.daemon = True
    sThread.start()

    rThread = threading.Thread(target=self.render)
    rThread.daemon = True
    rThread.start()

    while True:
      data = self.sock.recv(1024)
      if not data:
        print('server disconnected')
        break
      print(len(data))
      received = pickle.loads(data)
      print(received, '({} bytes)'.format(len(data)))
      if received.header == 'newFrame':
        self.points += received.body

def main(argv):
  client = Client(argv[0], int(argv[1]))
  client.run()

if __name__ == '__main__':
  main(sys.argv[1:])
