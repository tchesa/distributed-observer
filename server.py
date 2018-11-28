# responsável por gerenciar os pontos
# responsável por armazenar e notificar os observadores

import threading
import socket
from point import Point

class Server:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  subscribers = []
  host = '127.0.0.1'
  port = 5000

  def __init__(self):
    print('server initialized')
    self.sock.bind((self.host, self.port))
    self.sock.listen(1)

    t = threading.Thread(target=self.sendMsg)
    t.daemon = True
    t.start()

  def notifyAll(self, message):
    for subscriber in self.subscribers:
      subscriber.send(message.encode('utf8'))

  def sendMsg(self):
    while True:
      message = input('-> ')
      self.notifyAll(message)

  def handler(self, c, a):
    while True:
      data = c.recv(1024)
      # for connection in self.subscribers:
      #   connection.send(data)
      if not data:
        print(str(a[0]) + ':' + str(a[1]), 'disconnected')
        self.subscribers.remove(c)
        # break

  def run(self):
    while True:
      c, a = self.sock.accept()
      self.subscribers.append(c)
      print(str(a[0]) + ':' + str(a[1]), 'connected')

s = Server()
s.run()
