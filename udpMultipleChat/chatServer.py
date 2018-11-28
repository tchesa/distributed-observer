import socket
import time

host = '127.0.0.1'
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print('server started')

while not quitting:
  try:
    data, addr = s.recvfrom(1024)
    if 'Quit' in data.decode('utf8'):
      quitting = True
    if addr not in clients:
      clients.append(addr)
    print('{} - {}: :{}'.format(time.ctime(time.time()), addr, data.decode('utf8')))
    for client in clients:
      s.sendto(data, client)
  except:
    pass
s.close()
