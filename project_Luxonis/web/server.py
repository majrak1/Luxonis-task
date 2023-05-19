import http.server
import socketserver
import mysql.connector

# define the HTTP request handler
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        connection = mysql.connector.connect(
            user='root', password='root', host='mysql', port="3306", database='db')
        print("DB connected")

        # query database to get the names and urls of the images
        cur = connection.cursor()        
        cur.execute('SELECT title, url FROM apartment')
        rows = cur.fetchall()

        # Generate the HTML page from the database
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html lang='en'><head>", "UTF-8"))
        self.wfile.write(bytes("<meta charset='UTF-8'>", "UTF-8"))
        self.wfile.write(bytes("<meta http-equiv='X-UA-Compatible' content='IE=edge'>", "UTF-8"))
        self.wfile.write(bytes("<meta name='viewport' content='width=device-width, initial-scale=1.0'>", "UTF-8"))
        self.wfile.write(bytes("<title>Sreality Apartments</title>", "UTF-8"))
        self.wfile.write(bytes("</head>", "UTF-8"))
        self.wfile.write(bytes("<body>", "UTF-8"))
        for row in rows:
            self.wfile.write(bytes(f"<h2>{row[0]}</h2>", "UTF-8"))
            self.wfile.write(bytes(f"<img src='{row[1]}'<br>", "UTF-8"))                               
        self.wfile.write(bytes("</body></html>", "UTF-8"))


# Start the HTTP server
PORT = 8080
Handler = MyHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"Serving on port {PORT}")
httpd.serve_forever()
