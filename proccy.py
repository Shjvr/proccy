import http.server
import socket

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Get the URL from the request
        url = self.path

        # Connect to the target server
        conn = socket.create_connection((url, 80))

        # Send the GET request to the target server
        conn.sendall(b"GET " + url.encode() + b" HTTP/1.1\r\n")
        conn.sendall(b"Host: " + url.split("://")[1].encode() + b"\r\n")
        conn.sendall(b"\r\n")

        # Read the response from the target server
        response = conn.recv(4096)

        # Send the response back to the client
        self.wfile.write(response)

# Create a new HTTP server and set the handler class
httpd = http.server.HTTPServer(('', 80), ProxyHandler)

# Start the server
print("Starting proxy server...")
httpd.serve_forever()
