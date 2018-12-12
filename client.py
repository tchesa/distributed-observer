# responsável por receber as notificações do servidor
# responsável por armazenar e plotar os pontos recebidos

import socket
import threading
import pickle
from message import Message
from point import Point
import sys
import uuid
import numpy as np
import matplotlib.pyplot as plt
import time

class Client:
  points = []
  servers = []

  def __init__(self, host, port):
    self.servers.append((host, port,))

  def render(self):
    plt.axis([0, 10, 0, 10])
    print('shown')
    while True:
      for point in self.points:
        plt.scatter(point.x, point.y, c=point.c)
      plt.pause(0.05)
    plt.show()
      # plt.clf()

  def run(self):
    rThread = threading.Thread(target=self.render)
    rThread.daemon = True
    rThread.start()

    while len(self.servers) > 0:
      sock = socket.socket()
      try:
        print('trying to connect to {}:{}'.format(self.servers[0][0], self.servers[0][1]))
        sock.connect((self.servers[0][0], self.servers[0][1]))
      except:
        print("FAILED. Sleep briefly & try again")
        time.sleep(1)
        continue

      while True:
        data = sock.recv(1024)
        if not data:
          print('server disconnected')
          break
        received = pickle.loads(data)
        print(received, '({} bytes)'.format(len(data)))
        if received.header == 'greeting':
          sock.send(Message('getServers', '').encode())
        elif received.header == 'newFrame':
          self.points += received.body
        elif received.header == 'updateServers':
          self.servers = received.body
      self.servers.pop(0)

def main(argv):
  client = Client(argv[0], int(argv[1]))
  client.run()

if __name__ == '__main__':
  main(sys.argv[1:])
