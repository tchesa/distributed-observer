import socket

def main():
  host = '127.0.0.1'
  port = 5001

  s = socket.socket()
  s.bind((host, port))

  s.listen(1)
  c, addr = s.accept()
  print('connection from: ' + str(addr))
  while True:
    data = c.recv(1024)
    if not data:
      break
    data = data.decode('utf8')
    print('from connected user: ' + str(data))
    data = str(data).upper()
    print('sending: ' + str(data))
    c.send(data.encode('utf8'))
  c.close()

if __name__ == '__main__':
  main()
