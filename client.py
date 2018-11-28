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
  server = ('127.0.0.1', 5000)
  shutdown = False

  def sendMsg(self):
    while not self.shutdown:
      self.shutdown = input('exit (y/n)? ') == "y"
    # self.sock.close()

  def __init__(self, address):
    self.sock.connect(self.server)

    t = threading.Thread(target=self.sendMsg)
    t.daemon = True
    t.start()

    while not self.shutdown:
      try:
        data = self.sock.recv(1024)
        if not data:
          break
        print(data.decode('utf8'))
      except:
        print('error')

client = Client('127.0.0.1')
