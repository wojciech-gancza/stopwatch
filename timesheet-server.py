#!/usr/bin/python

# based on example form https://pythonbasics.org/webserver/

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import argparse

host_name = "localhost"
server_port = 8483
timesheet_path = ""

""" Access to local files """
class LocalFileAccess:

    @staticmethod 
    def getLocalFile(file_name, binary_read = False):
        try:
            mode = "r"
            if binary_read:
                mode = "rb"
            with open(file_name, mode) as file:
                return file.read()
        except Exception as e:
            print("File read exception: " + str(e))
            return None
            
    def storeLocalFile(file_name, content):
        with open(file_name, "w") as file:
            file.write(content)

""" Repository of timeseets data """
class Timeseets:

    @staticmethod 
    def getTimesheet(user_name):
        file_name = Timeseets._getCurrentTimesheetFileName(user_name)
        timesheet_file = LocalFileAccess.getLocalFile(file_name)
        if timesheet_file is None:
            timesheet_file = Timeseets.getDefaultTimesheet(user_name)
        return timesheet_file;
        
    @staticmethod
    def getDefaultTimesheet(user_name):
        file_name = Timeseets._getUserDefaultTimesheetFileName(user_name)
        default_file = LocalFileAccess.getLocalFile(file_name)
        if default_file is None:
            file_name = Timeseets._getDefaultTimesheetFileName()
            default_file = LocalFileAccess.getLocalFile(file_name)
        if default_file is None:
            return None
        data = json.loads(default_file)  
        if "task_list" in data.keys():
            for task in data["task_list"]:
                if "worked_time_in_seconds" not in task.keys():
                    task["worked_time_in_seconds"] = 0
        if "web_interface_data" not in data.keys():
            data["web_interface_data"] = { }
            data["web_interface_data"]["is_running"] = False
            data["web_interface_data"]["from_time"] = 0
            data["web_interface_data"]["current_task"] = 0            
        data["web_interface_data"]["user"] = user_name;
        return json.dumps(data)

    @staticmethod 
    def setTimesheet(data):
        parsed_data = json.loads(data)
        user_name = parsed_data["web_interface_data"]["user"]
        file_name = Timeseets._getCurrentTimesheetFileName(user_name)
        LocalFileAccess.storeLocalFile(file_name, data)
        
    @staticmethod
    def _getCurrentTimesheetFileName(user_name):
        return timesheet_path + datetime.now().strftime("%Y-%m-%d-") + user_name + ".json"

    @staticmethod
    def _getUserDefaultTimesheetFileName(user_name):
        return timesheet_path + "default-" + user_name + ".json"

    @staticmethod
    def _getDefaultTimesheetFileName():
        return timesheet_path + "global-default.json"

    @staticmethod
    def _getDefaultTimesheetFile(user_name):
        return datetime.now().strftime("%Y-%m-%d-") + user_name + ".json"

""" Web server serving stopwatch interface and handling data changes """
class StopwatchServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/favicon.ico":
            self._sendFavicon()
        else: 
            if self.path == '/':
                user_name = "unknown"
            else:
                user_name = self.path[1:]
            timesheet_data = Timeseets.getTimesheet(user_name)
            self._sendInterface(timesheet_data)
    
    def do_POST(self):
        data = self._getData()
        Timeseets.setTimesheet(data)
        self._sendResponse("OK")
    
    def _sendInterface(self, timesheet_data):
        www_interface = LocalFileAccess.getLocalFile("stopwatch.html")
        json_string_data = StopwatchServer._encode_to_string(timesheet_data)
        www_page = www_interface.replace(" ***** *** ", json_string_data)
        self._sendResponse(www_page)
        
    def _sendResponse(self, text):    
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(text, "utf-8"))
    
    def _sendFavicon(self):
        icon_data = LocalFileAccess.getLocalFile("favicon.ico", True)
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        self.end_headers()
        self.wfile.write(icon_data)
        
    def _getData(self):
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len)
        return data.decode("Utf-8")
        
    @staticmethod 
    def _encode_to_string(text):
        text = text.replace("\\", "\\\\")
        text = text.replace("\"", "\\\"")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        return text
        
    @staticmethod 
    def main():
        webServer = HTTPServer((host_name, server_port), StopwatchServer)
        print("Server started http://%s:%s" % (host_name, server_port))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
        webServer.server_close()
        print("Server stopped.")       

""" Just start web server when module is called as application """
if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help = "port server is listening on")
    parser.add_argument("-i", "--ip", help = "ip of the interface server is listening on")
    parser.add_argument("-s", "--storage", help = "directory where timesheet json files are stored (slash ending)")
    args = parser.parse_args()
 
    if args.port:
        server_port = int(args.port)
    if args.ip:
        host_name = args.ip
    if args.storage:
        timesheet_path = args.storage
        
    StopwatchServer.main()