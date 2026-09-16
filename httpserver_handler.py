import http.server, os, urllib
from db.database import create_connection, create_table, insert, fetch_all, addcolumn, close
from hypertexttransferprotocol.forms import get

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
            addcolumn(self.conn, "links", "title", "TEXT", "NOT NULL")
            addcolumn(self.conn, "links", "url", "TEXT", "NOT NULL")
            rows = ""
            for row in fetch_all(self.conn, "links", '*'):
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
                        placeholder="Enter email" minLength="11"
                        required>
                    <br>

                    <input type="phone" id="phone" name="phone"
                        placeholder="Enter phone number" minLength="9"
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
                phone TEXT NOT NULL UNIQUE
                    CHECK (
                        phone GLOB '([0-9][0-9][0-9]) [0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'
                    )
            """
            create_table(self.conn, "users", constraints)
            rows = ""
            for row in fetch_all(self.conn, "users", "*"):
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
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = ""
            with open('test.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            self.wfile.write(html_content.encode()) # encode means convert bytes to a string
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1><p>The page you are looking for does not exist.</p>')
            # b'string' is a convert to bytes string
    def do_POST(self):
        if self.path == '/links':
            content_length = int(self.headers.get('Content-length', 0))
            body_bytes = self.rfile.read(content_length)
            body_string = body_bytes.decode('utf-8')
            form_data = urllib.parse.parse_qs(body_string)
            
            title, url = get(form_data, 'title url', [''])
            
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
            # .get: if found returns the string
            #       if not found return empty string
            username, password, email, phone = get(form_data, 'user password email phone', [''])
            
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            
            response_html = f"<h1>Thanks</h1><p>{username}</p><p>{password}</p>"
            self.wfile.write(response_html.encode('utf-8'))
            
            self.conn = create_connection("links_db.sql")
            insert(self.conn, "users", "username, password, email, phone", f"\'{username}\', \'{password}\', \'{email}\', \'{phone}\'")
            close(self.conn)
