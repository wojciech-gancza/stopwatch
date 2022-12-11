# copy-past example form https://pythonbasics.org/webserver/
# then made some modifications to return and process timesheet
# processing

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

""" Repository of timeseets data """
class Timeseets:

    def __init__(self):
        pass

""" Web server serving stopwatch interface and handling data changes """
class StopwatchServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/favicon.ico":
            self._sendFavicon()
        else: 
            timesheet_data = StopwatchServer._getLocalFile("example.data.json")
            self._sendInterface(timesheet_data)
    
    def do_POST(self):
        data = self._getData()
        print("Recived: " + data)
        self._sendResponse("OK")
    
    def _sendInterface(self, timesheet_data):
        www_interface = StopwatchServer._getLocalFile("stopwatch.html")
        json_string_data = StopwatchServer._encode_to_string(timesheet_data)
        www_page = www_interface.replace(" ***** *** ", json_string_data)
        self._sendResponse(www_page)
        
    def _sendResponse(self, text):    
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(text, "utf-8"))
    
    def _sendFavicon(self):
        icon_data = StopwatchServer._getLocalFile("favicon.ico", True)
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        self.end_headers()
        self.wfile.write(icon_data)
        
    def _getData(self):
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len)
        return data.decode("Utf-8")
        
    @staticmethod 
    def _getLocalFile(file_name, binary_read = False):
        try:
            mode = "r"
            if binary_read:
                mode = "rb"
            with open(file_name, mode) as file:
                return file.read()
        except Exception as e:
            print("File read exception: " + str(e))
            return None
    
    @staticmethod 
    def _encode_to_string(text):
        text = text.replace("\\", "\\\\")
        text = text.replace("\"", "\\\"")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        return text
        
    @staticmethod 
    def main():
        webServer = HTTPServer((hostName, serverPort), StopwatchServer)
        print("Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
        webServer.server_close()
        print("Server stopped.")       

""" Just start web server when module is called as application """
if __name__ == "__main__":        
    StopwatchServer.main()