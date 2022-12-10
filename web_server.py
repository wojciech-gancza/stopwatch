# copy-past example form https://pythonbasics.org/webserver/
# then made some modifications to return and process timesheet
# processing

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("stopwatch.html") as file:
            www_interface = file.read()
        with open("example.data.json") as file:
            timesheet_data = file.read() 
        www_page = www_interface.replace(" ***** *** ", self.encode_to_string(timesheet_data))
        self.wfile.write(bytes(www_page, "utf-8"))
    
    def encode_to_string(self, text):
        text = text.replace("\\", "\\\\")
        text = text.replace("\"", "\\\"")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        return text

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")