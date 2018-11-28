import socket

def main():
  host = '127.0.0.1'
  port = 5000

  s = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
  s.bind((host, port))

  print('server started')
  while True:
    data, addr = s.recvfrom(1024)
    data = data.decode('utf8')
    print('message from: ' + str(addr))
    print('from connected user: ' + data)
    data = str(data).upper()
    s.sendto(data.encode('utf8'), str(addr))
  s.close()

if __name__ == '__main__':
  main()
