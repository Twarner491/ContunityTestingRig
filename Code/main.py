#sources:
#https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/
#https://www.tomshardware.com/how-to/raspberry-pi-pico-w-web-server


#todo
#set up hardware button for launch site
#set up html template
#set up svg file template
#write method to edit fill variable to svg and assign to variable

#add -1 case for getHeaderFormat (header file incorrectly formatted, push error to site)
#add -2 case for getHeaderFormat (no file found, push error to site)
#add returns 0 confirmation for getHeaderFormat
#run checkPinout() differently based on numPins from headerformat
#add -2 case for getSVGFormat (no format file found)
#add returns 0 confirmation for getSVGFormat
#<g> group header for adding text labels to svg pin objects
#determine if header config file is necessary, do they want a specific config for each header type?


#write and implements javascript script to take button input from site
#use ajax library in javascript to send input to python
#https://stackoverflow.com/questions/42841281/how-to-make-a-button-in-html-that-can-trigger-backend-functions-in-python


import rp2
from machine import Pin
import utime

import socket
import network
import sys
import Functions
#file with defined functions, micropython is a top-down language and there was poor readability
#when having all functions defined above the main code 


ssid = 'secure'
password = 'griggssecure'


inPinNums = [2,3,4,5]
outPinNums = [6,7,8,9,10,11,12,13,14]
GPIOpins = [[],[]]
buttonPin = Pin(26,Pin.OUT, Pin.PULL_DOWN)


def updateSite():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Wait fo
    # r connect or fail
    max_wait = 15
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      utime.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0])      
    page = open("index.html","r")
    html = page.read()
    page.close()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print("listening on", addr)
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        pinoutList = Functions.checkPinout(GPIOpins)
        rows = []
        for i in range(len(pinoutList[1][0])):
            pinoutStr = "Pin " + str(pinoutList[1][0][i]) + " --> Pin " + str(pinoutList[1][1][i])
            print(pinoutStr)
            rows.append('<body> <br> %s </br> </body>' % pinoutStr)
        svgs = []
        headerformat = Functions.getHeaderFormat()
        colors = headerformat[1]
        svgpins = Functions.getSVGFormat(colors)
        if(svgpins == -2):
            svgs.append('<body><br>No SVG Format File Found</br></body>')
        else:
            for i in range(len(svgpins)):
                svgs.append('<body> <br> %s </br> </body>' % svgpins[i])
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
    #    rows = '<body> %s </body>' % pinoutStr
        response = html
        for i in range(len(rows)):
            response += rows[i]
        for i in range(len(svgs)):
            response += svgs[i]
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()




#    if(buttonPin.value() == 1 || software button pressed)
pins = Functions.setup(inPinNums,outPinNums)
GPIOpins[0].append(pins[0])
GPIOpins[1].append(pins[1])
#nwrk = Functions.ntwkconnect(ssid, password)
#Functions.updateSite()    

#if(nwrk == -1):
#    raise RuntimeError('network connection failed')
#elif(nwrk[0] == 0):
#    print("connected. ip:" + nwrk[1])
updateSite()
#Functions.updateSite()