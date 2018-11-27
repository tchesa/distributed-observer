# responsável por gerenciar os pontos
# responsável por armazenar e notificar os observadores

import threading
import socket
from point import Point

class Server:
  subscribers = []

  def __init__(self):
    print('server initialized')

  def notifyAll(self):
    for subscriber in self.subscribers:
      'do something'
