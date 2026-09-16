import os, http.server, threading, socketserver, urllib
from db.database import create_connection, create_table, insert, fetch_all, addrow, close

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
            create_table(self.conn, "links", "")
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
            # Emails HTML5 Validation 
            # theoretical minimum (intranet/private systems) 3 characters (a@b)
            # Practical internet minimum: 6 characters (i@g.cn) 
            # Service specific minimums (e.g., Gmail) 11 characters (abc123@gmail.com)
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Signup Page</title>
                <link rel='stylesheet' href='/style.css'>
            </head>
            <body>
                <h1>Signup Page</h1>
                <form method="POST" action="/signup">
                    <label for="user">
                        Enter your username
                    </label>
                    <input type="text" id="user" name="user" 
                        placeholder="Enter username" required>
                    <br>
                    
                    <label for="password">
                        Enter your password
                    </label>
                    <input type="password" id="password" name="password" 
                        placeholder="Enter password" minLength="8" required>
                    <br>

                    <label for="email">
                        Enter your email
                    </label>
                    <input type="email" id="email" name="email"
                        placeholder="Enter email" minLength="11""
                        required>
                    <br>

                    <input type='checkbox' name='remember'>
                        Remember me
                    </input>
                    
                    <button type="submit"> Sign up </button>
                </form>
            </body>
            </html>
            """
            self.conn = create_connection("links_db.sql")
            constraints = """
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL 
                    CHECK (
                        -- Must contain at least one uppercase letter
                        password GLOB '*[A-Z]*'
                        AND
                        -- MUST contain at least one special character from this set
                        password GLOB '*[!@#$%&*+]*'
                    ),
                email TEXT NOT NULL UNIQUE
                    CHECK (
                        email LIKE '%_@_%._%' AND
                        LENGTH(email) - LENGTH(REPLACE(email, '@', '')) = 1 AND
                        SUBSTR(LOWER(email), 1, INSTR(email, '.') - 1) NOT GLOB '*[^@0-9a-z]*' AND
                        SUBSTR(LOWER(email), INSTR(email, '.') + 1) NOT GLOB '*[^a-z]*'
                    ),
                phone TEXT NOT NULL 
                    CHECK (
                        number GLOB '([0-9][0-9][0-9]) [0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'
                    ),
            """
            create_table(self.conn, "users", "")
            rows = ""
            for row in fetch_all(self.conn, "users"):
                rows += f"""
                <p>ID: {row[0]} User: {row[1]} PW: {row[2]} Email: {row[3]} Phone Number: {row[4]}
                """
            close(self.conn)
            html_content += "<div>\n" + rows + "</div>"
            # self.send_header('Set-Cookie')
            self.wfile.write(html_content.encode())
            close(self.conn)
        elif self.path == '/login':
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
