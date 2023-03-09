#(c) Drew Griggs & Teddy Warner - (2023)

#This work may be reproduced, modified, distributed, performed, and displayed
#for any purpose, but must acknowledge Teddy Warner.
#Copyright is retained and must be preserved. The work is provided as is;
#no warranty is provided, and users accept all liability.

import machine
import rp2
from machine import Timer
from machine import Pin
import utime
import socket
import network


ssid = 'CLSLabs'
password = 'clshawks'


inPinNums = [3,4,5,6]
inputPins = []

nmosCtrl = [7,8,9,10,17,18,19,20,21,22,26,27,28]
nmosCtrlPins = []

outPinsInNmos = [13,12,11,10,9,8,7,6,5] #index of nmos pins for 9 pin header

for i in range(len(inPinNums)):
    inputPins.append(Pin(inPinNums[i], Pin.IN, Pin.PULL_DOWN))

for i in range(len(nmosCtrl)):
    nmosCtrlPins.append(Pin(nmosCtrl[i], Pin.OUT))

ledPin = Pin(11,Pin.OUT)


def getSVGFormat(pinout):
    pinoutArray = [[],[]]
    for i in range(len(pinout[1])):
        lowVal = pinout[1][0]
        lowIndex = 0
        for j in range(len(pinout[1])):
            if(pinout[1][j] < lowVal and pinout[1][j] != 0):
                lowVal = pinout[1][j]
                lowIndex = j
        pinoutArray[0].append(pinout[0][lowIndex])
        pinoutArray[1].append(pinout[1][lowIndex])
        pinout[0].pop(lowIndex)
        pinout[1].pop(lowIndex)
    pinout = pinoutArray
    colors = ["e3342f","f6993f","ffed4a","38c172","4dc0b5","3490dc","6574cd","9561e2","f66d9b"]
    svgfile = '<svg width="250" height="250" viewBox="0 0 175 175"><rect x="20" y="0" width="35" height="35" fill="#000"/><rect x="65" y="0" width="35" height="35" fill="#000"/><rect x="110" y="0" width="35" height="35" fill="#000"/><rect x="0" y="45" width="35" height="35" fill="#000"/><rect x="45" y="45" width="35" height="35" fill="#000"/><rect x="90" y="45" width="35" height="35" fill="#000"/><rect x="135" y="45" width="35" height="35" fill="#000"/><rect x="0" y="90" width="35" height="35" fill="#000"/><rect x="45" y="90" width="35" height="35" fill="#000"/><rect x="90" y="90" width="35" height="35" fill="#000"/><rect x="135" y="90" width="35" height="35" fill="#000"/><rect x="45" y="135" width="35" height="35" fill="#000"/><rect x="90" y="135" width="35" height="35" fill="#000"/></svg>'
    reformat = svgfile.split('fill="#000"')
    finalSVG = ""
    pinindex = 0
    for i in range(13):
        finalSVG += reformat[i]
        found = False
        for j in range(9):
            if(pinout[1][j] == (i + 1)):
                found = True
                finalSVG += 'fill ="#' + colors[pinout[0][j]-1] + '"'
        if(not found):
            finalSVG += 'fill ="#212124"'
    finalSVG += reformat[-1]
    return finalSVG


def updateSite():   
    page = open("index.html","r")
    html = page.read()
    page.close()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        pinoutList = checkPinout()
        rows = []
        for i in range(len(pinoutList[0])):
            pinoutStr = "Pin " + str(pinoutList[0][i]) + " 🠚 Pin " + str(pinoutList[1][i])
            rows.append('<p class="pinoutprint"> %s </p>' % pinoutStr)
#        svgs = []
#        getHeaderFormat()
#        getSVGFormat()
#        for i in range(len(svgpins)):
#            svgs.append('<body> <br> %s </br> </body>' % svgpins[i])
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html
        stringrows = ''
        for i in range(len(rows)):
            stringrows += rows[i]
        splitresponse = response.split('<!-- Split Spot 1 -->')
        response = splitresponse[0] + stringrows + splitresponse[1]
        splitresponse = response.split('<!-- Split Spot 2 -->')
        response = splitresponse[0] + getSVGFormat(checkPinout()) + splitresponse[1]
        #for i in range(len(svgs)):
         #   response += svgs[i]
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

def networkConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Wait for connect or fail
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
      print( 'ip = ' + status[0] )


def bin2num():
    p1 = inputPins[0].value()
    p2 = inputPins[1].value()
    p3 = inputPins[2].value()
    p4 = inputPins[3].value()
    return (p1 + p2*2 + p3*4 + p4*8)


def checkPinout():
    pinout = [[],[]]
    for i in range(len(outPinsInNmos)):
        nmosCtrlPins[outPinsInNmos[i]-1].value(1)
        pinout[0].append(i+1)
        pinout[1].append(bin2num())
        nmosCtrlPins[outPinsInNmos[i]-1].value(0)
    return pinout
           
networkConnect()
updateSite()