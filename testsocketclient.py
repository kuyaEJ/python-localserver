import socket
s = socket.socket()
host = socket.gethostname()
port = 8080
s.connect((host, port)) # May raise ConnectionRefusedError if server not listening
print(s.recv(1024))
s.close()