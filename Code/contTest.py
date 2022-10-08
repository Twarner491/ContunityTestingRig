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
#-----------------------------------------------------------------------------------------------------------------------------------------

import machine
import rp2
from machine import Timer
from machine import Pin
import utime


inPinNums = [4,5,6,7]
#gpio input pins
outPinNums = [9,10,11,12,14,15,16,17,19]
#gpio output pins

inputPins = [0,0,0,0]
#empty pin object array (input)
    
outputPins = [0,0,0,0,0,0,0,0,0,0,0,0,0]
#empty pin object array (output)

pinout = [[1,2,3,4,5,6,7,8,9], [0,0,0,0,0,0,0,0,0]]
#pin configuration

for i in range(len(inPinNums)):
    inputPins[i] = Pin(inPinNums[i], Pin.IN)
    #fill input pin object array with new pin object

for i in range(len(outPinNums)):
    outputPins[i] = Pin(outPinNums[i], Pin.OUT)
    #fill output pin object array with new pin object



def checkPinout():
    r = "Pinout:/n"
    #String to return
    
    for i in range(len(outputPins)):
#    increment through output pins
        outputPins[i-1].high()
        #set pin to high
        utime.sleep(0.01)
        #small delay before read
        p1 = inputPins[0].value()
        p2 = inputPins[1].value()
        p3 = inputPins[2].value()
        p4 = inputPins[3].value()
        #input pin value (high = 1, low = 0) is set to variable
        outputPins[i-1].low()
        #reset pin

        pin = bin2num(p1, p2, p3, p4)
        #set pin to its binary equivalent (4 bit, p4*8 + p3 * 4 + p2 * 2 + p1 * 1)
        pinout[1][i] = pin
        #set second row of corresponding pin in pinout to the resulting pin value
        
        r += "Pin " + i + " --> Pin " + pin + "/n"
        #build string equivalent to array
        
    return [pinout, r]
#return list including array and string

def bin2num(a, b, c, d):
    z = a
    z += b << 1
    z += c << 2
    z += d << 3
    #add the equivalent value of the bit (0 << 3 = 0, 1 << 3 = 1000 = 8)
    return z
    #return the equivalent pin value


print(checkPinout())
#debug code