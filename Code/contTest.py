#Continuity Tester Python Script
#
#Developed by Drew Griggs and Teddy Warner
#
#
#Alongside the hardware diode array, this script tests the pinout of variable headers by writing and reading from the 
#GPIO pins of a raspberry pi pico. Prints into UART a 2x9 array of the pinout, with the pins designated by the nth
#column of the array being connected, and a visual equivalent string.
#
#Requires a hardware array of diodes to convert designated pins (ours is capable of handling up to 16 pins) into their 4 bit
#binary equivalent (pin 5 would have pins 1 and 3 high, and pins 2 and 4 low), the pico will write a pin on one end of the header to high
#and read this binary value
#
#Setup for raspberry pi pico found on this website:
#https://www.tomshardware.com/how-to/raspberry-pi-pico-setup
#
#
#TODO:
#Build Static Site
#Read from Static Site
#Edit HTML File and Republish Site
#-----------------------------------------------------------------------------------------------------------------------------------------

#import machine
import rp2
#from machine import Timer
from machine import Pin
import utime

inPinNums = [3,4,5,6] #gpio input pins
outPinNums = [7,8,9,10,11,12,13,14,15] #gpio output pins

inputPins = [] #empty pin object array (input)
outputPins = []

for i in range(len(inPinNums)):
    inputPins.append(Pin(inPinNums[i]), Pin.IN) #fill input pin object array with new pin object

for i in range(len(outPinNums)):
    outputPins.append(Pin(outPinNums[i], Pin.OUT))
    outputPins[i].value(0) #default value
    
def checkPinout():
    r = "Pinout:"
    #String to return
    
    for i in range(len(outputPins)):
#    increment through output pins
        try:
            outputPins[i].value(1)         #set pin to high
        
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
            utime.sleep(0.01) #reset pin

        pin = bin2num(p1, p2, p3, p4) #set pin to its binary equivalent (4 bit)
        pinout[1][i] = pin #set corresponding pin row in pinout to the resulting pin number
        
        r += "Pin " + str(i) + " --> Pin " + str(pin) #build string equivalent to array (display purposes)
      
    return [pinout, r] #return list including array and string

def bin2num(a, b, c, d):
    z = a
    z += b << 1
    z += c << 2
    z += d << 3
    #add the equivalent value of the bit (0 << 3 = 0, 1 << 3 = 1000 = 8)
    return z
    #return the equivalent pin value

#STATIC SITE SETUP

while True:
    #check button for static site launch
#     (maybe add button to gpio pins to initialize static site instead of generate when connected to power)
        #launch static site
    #check static site for pinout request
        #checkPinout()
        #build html file based on pinout
        #push new html file to static site