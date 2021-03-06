# this script is for python3. https://gist.github.com/nitaku/10d0662536f37a087e1b
# to run it :
# python3 velodyne_ser.py 8080
# to use curl get data:
# curl http://localhost:8080

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        # velodyne json status.
        json_msg = '{"gps":{ "pps_state":"Absent", "position":"" }, "motor":{ "state":"On", "rpm":600, "lock":"Off", "phase":0 }, "laser":{ "state":"On" } }'
        parsed = json.loads(json_msg)
        self.wfile.write(json.dumps(parsed, indent=4, sort_keys=True).encode('utf-8'))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('127.0.0.2', port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        try:
            run()
        except KeyboardInterrupt:
            exit