#sources:
#https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/
#https://www.tomshardware.com/how-to/raspberry-pi-pico-w-web-server


#todo
#set up hardware button for launch site
#set up html template
#set up svg file template
#write method to edit fill variable to svg and assign to variable

import rp2
from machine import Pin
import utime

import socket
import network


ssid = 'CLSLabs'
password = 'clshawks'



bool hasBeenSetup = false


setup()
def main():
    if(hardware button pressed && !hasBeenSetup)
    connect()
    updateSite()



 
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
        pinoutList = checkPinout()[1]
        rows = []
        for i in range(len(pinoutList[0])):
            pinoutStr = "Pin " + str(pinoutList[0][i]) + " --> Pin " + str(pinoutList[1][i])
            rows.append('<body> <br> %s </br> </body>' % pinoutStr)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
    #    rows = '<body> %s </body>' % pinoutStr
        response = html
        for i in range(len(rows)):
            response += rows[i]
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
      
def connect():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)


def setup(): #pin setup
    #gpio pin numbers
    inPinNums = [2,3,4,5]
    outPinNums = [6,7,8,9,10,11,12,13,14]
    #create and fill arrays of pin objects, pinout array
    inputPins = []
    outputPins = []
    for i in range(len(inPinNums)):
        inputPins.append(Pin(inPinNums[i], Pin.IN)) #fill input pin object array with new pin object
    for i in range(len(outPinNums)):
        outputPins.append(Pin(outPinNums[i], Pin.OUT))
        outputPins[i].value(0) #default value
    connectNetwork()

def checkPinout():
    pinout = [[],[]]
    for i in range(len(outputPins)):
        pinout[0].append(i+1) #start building pinout array
    r = "Pinout:"
    #String to return
    for i in range(len(outputPins)):
        try:
            outputPins[i].value(1) #set pin to high
        except:
            utime.sleep(0.01)
        utime.sleep(0.01)
        p1 = inputPins[0].value()
        p2 = inputPins[1].value()
        p3 = inputPins[2].value()
        p4 = inputPins[3].value() #read input pin value (high = 1, low = 0)
        try:
            outputPins[i].value(0) #reset pin to low
        except:
            utime.sleep(0.01)
        pin = bin2num(p1,p2,p3,p4)
        pinout[1].append(pin) #set pinout pin to binary equivalent of inputs
        r += "Pin " + str(i) + " --> Pin " + str(pin) + '\n' #build string equivalent to array (display purposes)
    return [r,pinout]

def bin2num(a, b, c, d):
    z = a
    z += b << 1
    z += c << 2
    z += d << 3
    #add the equivalent value of the bit
    return z
    #return the equivalent pin value