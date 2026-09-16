import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind((socket.gethostname(), 8080))
    sock.listen(5)
    while True:
        c, addr = sock.accept()
        print("Got connection from", addr)
        c.send(b"Hello Client")
        c.close()
except ConnectionRefusedError:
    print("Connection refused")
except KeyboardInterrupt:
    print("\nServer closed with KeyboardInterrupt!")
    sock.close()