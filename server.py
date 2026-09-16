import os, threading, socketserver, urllib
from httpserver_handler import MyHandler


class TCPServer(socketserver.TCPServer):
    pass

TCPServer.allow_reuse_address = True
port = 4040
# if len(sys.argv) > 1:
#     if sys.argv[1]:
#         try:
#             port = int(sys.argv[1])
#         except Exception as e:
#             print("Usage: python server.py <port>")
#             print(f'Port number error: {e}')
#             sys.exit(1)


# Ensure server is properly acquired and released 
# with server as httpd:
#   httpd.server_forever()
server = TCPServer(('127.0.0.1', port), MyHandler)

def run_server():
    with server:
        server.serve_forever()

def close_server():
    with server:
        server.server_close()

try:
    # 
    # threading.Thread(target = run_server, daemon = True).start()
    #
    # daemon ensures the thread exits when the main program does
    # however in our code since the main program doesn't block then the thread ends
    #
    # Using a thread prevents the main thread from blocking and not running
    # any code afterwards.
    #
    # If we didn't use threads then print(f'Running TCPServer at port {port}')
    # would not run.
    print(f'Running TCPServer at port {port}')
    run_server()
    # threading.Thread(target = run_server).start()
    # print(f'Running TCPServer at port {port}')
except Exception as e:
    # print(e)
    pass
except KeyboardInterrupt:
    try:
        threading.Thread(target = close_server).start()
    except Exception as e:
        pass
    print("\nServer stopped")