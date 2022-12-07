import sys
import rp2
from machine import Pin
import network
import socket
import utime

inputPins = []
outputPins = []



#main site function

def updateSite():   
    page = open("index.html","r")
    html = page.read()
    page.close()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen()
    print("listening on", addr)
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        pinoutList = checkPinout(0)[1]
        rows = []
        for i in range(len(pinoutList[0])):
            pinoutStr = "Pin " + str(pinoutList[0][i]) + " --> Pin " + str(pinoutList[1][i])
            rows.append('<body> <br> %s </br> </body>' % pinoutStr)
        svgs = []
        getHeaderFormat()
        svgpins = getSVGFormat()
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






#setup functions

def ntwkconnect(netssid, netpw):
    ssid = netssid
    password = netpw
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
        return -1
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0])
        return [0,status[0]]

def setup(inPinNums,outPinNums): #pin setup
    #gpio pin numbers
    inPins = inPinNums
    outPins = outPinNums
    #create and fill arrays of pin objects, pinout array
    inputPins = []
    outputPins = []
    for i in range(len(inPins)):
        inputPins.append(Pin(inPins[i], Pin.IN)) #fill input pin object array with new pin object
    for i in range(len(outPins)):
        outputPins.append(Pin(outPins[i], Pin.OUT))
        outputPins[i].value(0) #default value
    return (inputPins, outputPins)






#Pin test functions

def checkPinout(GPIOpins):
    pinout = [[],[]]
    outputPins = GPIOpins[1][0] #weird way functions pass arguments
    inputPins = GPIOpins[0][0]
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




#formatting functions

def getHeaderFormat(headertype):
    colorformat = [[],[]]
    colors = []
    numPins = []
    with open("headerformat.txt", "r") as file: #basically a try catch loop
        headerlist = file.read() #read headerformat text file
        file.close()
        headerlist = headerlist.split('\n')
        match headertype:
            case "2":
                headerlist = headerlist[0]
            case "4":
                headerlist = headerlist[1]
            case "L":
                headerlist = headerlist[2]
            case _:
                print("no file go work or header type bad")
        headerlist = headerlist[2:]
        splitHeader = headerlist.split(' ') #split by space
        colors = splitHeader[1][1:(len(splitHeader[1])-1)].split(',') #colors list is set to the colors defined in the format file
        numPins = splitHeader[0][1:(len(splitHeader[0])-1)].split(',')
        numofpins = 0
        for i in range(len(numPins)):
            numofpins += int(numPins[i])
        if(int(len(colors))!= numofpins): #check if the format is correct, else ask to reformat
            print("Missing pin colors, add 'EMPTY' for a disconnected pin in the header")
            return -1 #incorrect header format error case
        return numPins, colors
    return -2 #no file error case

def getSVGFormat(colorcodes):
    svgcolors = colorcodes
    with open("13PinHeader.svg","r") as file:
        svgfile = file.read()
        file.close()
        reformat = svgfile.split('fill="#000000"')
        svgpins = ""
        while len(reformat) > 1:
            colorx = svgcolors.pop(0)
            if(colorx == "EMPTY"):
                colorx = "9BC"
            svgpins += reformat.pop(0) + 'fill="#' + colorx + '"'
        svgpins += reformat.pop()
        return svgpins
    return -2
