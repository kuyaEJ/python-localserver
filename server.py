import os, http.server, threading, socketserver, urllib
from modules.db.database import create_connection, create_table, insert, fetch_all, addrow, close

# Route Dict
# key' (route path): (func1, None) 
# Values are either func or None (GET, POST)
ROUTE_GET_REQUESTS = {
    '/': (None, None),
    '/help': (None, None),
    '/links': (None, None),
    '/signup': (None, None),
}

# Use one of these two formats
# 'key': lambda: func(args)
# 'key': func

class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello World')
            # threading.Thread(target=self.server.shutdown).start()
        elif self.path == '/help':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'This is the help section')

        elif self.path == '/links':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
            <form method="POST" action="/links">
                <input type="text" name="url" placeholder="Enter URL">
                <input type="text" name="title" placeholder="Enter title">
                <button type="submit">Save Link</button>
            </form>
            """
            self.conn = create_connection("links_db.sql")
            create_table(self.conn, "links")
            addrow(self.conn, "links", "title", "TEXT", "NOT NULL")
            addrow(self.conn, "links", "url", "TEXT", "NOT NULL")
            rows = ""
            for row in fetch_all(self.conn, "links"):
                rows += f"""
                <p>ID: {row[0]} Title: {row[1]} URL: {row[2]}
                """
            close(self.conn)
            html_content += "<div>\n" + rows + "</div>"
            self.wfile.write(html_content.encode())
        elif self.path == '/signup':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
            <h1>Signup Page</h1>
            <form method="POST" action="/signup">
                <input type="text" name="user" placeholder="Enter username: ">
                <input type="text" name="password" placeholder="Enter password: ">
                <button type="Submit">Login</button>
            </form>
            """
            self.conn = create_connection("links_db.sql")
            create_table(self.conn, "users")
            addrow(self.conn, "users", "username", "TEXT", "NOT NULL")
            addrow(self.conn, "users", "password", "TEXT", "NOT NULL")
            rows = ""
            for row in fetch_all(self.conn, "users"):
                rows += f"""
                <p>ID: {row[0]} User: {row[1]} PW: {row[2]}
                """
            close(self.conn)
            html_content += "<div>\n" + rows + "</div>"
            # self.send_header('Set-Cookie')
            self.wfile.write(html_content.encode())
            close(self.conn)
        elif self.path == 'login':
            pass
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1><p>The page you are looking for does not exist.</p>')

    def do_POST(self):
        if self.path == '/links':
            content_length = int(self.headers.get('Content-length', 0))
            body_bytes = self.rfile.read(content_length)
            body_string = body_bytes.decode('utf-8')
            form_data = urllib.parse.parse_qs(body_string)
            title = form_data.get('title', [''])[0]
            url = form_data.get('url', [''])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            response_html = f"<h1>Thanks</h1><p>{url.lower()}</p><p>{title}</p>"
            self.wfile.write(response_html.encode('utf-8'))
            self.conn = create_connection("links_db.sql")
            insert(self.conn, "links", "title, url", f"\'{title}\', \'{url.lower()}\'")
            close(self.conn)
        elif self.path == '/signup':
            content_length = int(self.headers.get('Content-length', 0))
            # b'user=u&password=p'
            body_bytes = self.rfile.read(content_length)
            # user=p&password=p
            body_string = body_bytes.decode('utf-8')
            # urllib makes a dictionary {} and places
            # the query params inside with the values
            # being inside a array even if there is 
            # no other values for the key included
            # e.g
            # {'user':['u'], 'password':['p']}
            # {'title':['title','title2'], 'url':['url']}  
            form_data = urllib.parse.parse_qs(body_string)
            username = form_data.get('user', [''])[0]
            password = form_data.get('password', [''])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            response_html = f"<h1>Thanks</h1><p>{username}</p><p>{password}</p>"
            self.wfile.write(response_html.encode('utf-8'))
            self.conn = create_connection("links_db.sql")
            insert(self.conn, "users", "username, password", f"\'{username}\', \'{password}\'")
            close(self.conn)


class TCPServer(socketserver.TCPServer):
    pass

TCPServer.allow_reuse_address = True
httpd = TCPServer(('127.0.0.1', 4040), MyHandler)

try:
    httpd.serve_forever()
    print(f'Running TCPServer at port 4040')
except KeyboardInterrupt:
    threading.Thread(target = httpd.server_close).start()
    print("\nServer stopped")
