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

import socket
import threading

class Client:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 8080

  def sendMsg(self):
    while True:
      self.sock.send(input('-> ').encode('utf8'))

  def __init__(self, address):
    self.sock.connect((address, self.port))

    t = threading.Thread(target=self.sendMsg)
    t.daemon = True
    t.start()

    while True:
      data = self.sock.recv(1024)
      if not data:
        break
      print(data.decode('utf8'))

client = Client('127.0.0.1')
