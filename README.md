Stopwatch - simple timeseet application
=======================================

Stopwatch is simple timesheet interface application. It makes timeshet controll easy
to note work time on different tasks. It is specially designed for users who often 
switches activity during work day.

# Running application

To start using timesheet stopwatch just start its web server. You can do it from command line or prepare configuration of a service. Starting from command line is easy:

`python timesheet-server.py`

To open timesheet in web browser - just type its address in adres bar:

`http://localhost:8483/`

Browser window content should look like











Stopwatch is simple webserver written in python. To access timesheet interface, open page:
<HOST>:8080/<USERNAME>, where <host} is the host you run web_server.py. <USERNAME> is 
the id of the timeseet user. Users do not need to be registered. When data for the user 
does not exist, default data are provided. 

All data are stored in ordinary json files. File name contain date of timesheet and user id: 
<YYYY-MM-DD>-<USERNAME>.json. When file does not exist - it is created based on "default-<USERNAME>.json"
or "global-defauld.json", if user specific default file does not exist.

Each change of data in interface is reflected in stored files. Files are not deleted by the 
stopwatch server. 

Data file format is simple, but some information might be important if you want to use timesheet data
in your application.
- Time is denoted and count of seconds.
