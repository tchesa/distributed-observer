import socket
import time
import threading

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
  while not shutdown:
    try:
      tLock.acquire()
      while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode('utf8'))
    except:
      pass
    finally:
      tLock.release()

host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=('RecvThread', s))
rT.start()

alias = input('Name: ')
message = input(alias + "'s: ")
while message != 'q':
  if message != '':
    s.sendto(str(alias + ': ' + message).encode('utf8'), server)
    tLock.acquire()
    message = input(alias + "'s: ")
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()
