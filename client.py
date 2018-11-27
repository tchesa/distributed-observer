# responsável por receber as notificações do servidor
# responsável por armazenar e plotar os pontos recebidos

# from point import Point

# class Client:
#   points = []

#   def __init__(self):
#     self.points = []

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 10])

for i in range(1000):
  x = np.random.random()*10
  y = np.random.random()*10
  plt.scatter(x, y)
  plt.pause(0.05)

plt.show()
