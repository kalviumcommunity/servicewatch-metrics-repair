import json
from http.server import BaseHTTPRequestHandler,HTTPServer
requests=0
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        global requests
        if self.path=="/metrics":
            data=("# HELP servicewatch_requests_total Requests to the demo endpoint.\n# TYPE servicewatch_requests_total counter\nservicewatch_requests_total "+str(requests)+"\n").encode();code=200;ctype="text/plain; version=0.0.4"
        elif self.path=="/demo":
            requests+=1;data=json.dumps({"status":"ok"}).encode();code=200;ctype="application/json"
        else: data=b'{"status":"alive"}';code=200;ctype="application/json"
        self.send_response(code);self.send_header("Content-Type",ctype);self.end_headers();self.wfile.write(data)
HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
