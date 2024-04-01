#! /usr/bin/env python3

"""
To Run - python input_test.py from a terminal window
All inputs that can be used by Pi Presents from model b+ onwards will be read every second
and their activation state printed to the terminal
The pins are configured for buttons wired between the pin and 0 volts, internal pullup is to 3.3 volts
Output:

   Board Name - The name of the pin on the physical 40 pin connector
   GPIO Name - The GPIO name used by gpiozero
   Pressed  - the state of the pin, 1 = pressed, 0 = not pressed
   
To exit type CTRL-C
"""

import sys
if sys.version_info[0] != 3:
        sys.stdout.write("ERROR: Pi Presents requires python 3\nHint: python3 input_test.py .......\n")
        exit(102)

from gpiozero import DigitalOutputDevice,Button
from time import sleep


#PINLIST = ['P1-03','P1-05','P1-07','P1-08',
#                'P1-10','P1-11','P1-12','P1-13','P1-15','P1-16','P1-18','P1-19',
#                'P1-21','P1-22','P1-23','P1-24','P1-26']

PINLIST = ['P1-03','P1-05','P1-07','P1-08',
                'P1-10','P1-11','P1-12','P1-13','P1-15','P1-16','P1-18','P1-19',
                'P1-21','P1-22','P1-23','P1-24','P1-26',
                'P1-29','P1-31','P1-32','P1-33','P1-35','P1-36','P1-37','P1-38','P1-40']

                
BOARDMAP = {'P1-03':2,'P1-05':3,'P1-07':4,'P1-08':14,
               'P1-10':15,'P1-11':17,'P1-12':18,'P1-13':27,'P1-15':22,'P1-16':23,'P1-18':24,'P1-19':10,
               'P1-21':9,'P1-22':25,'P1-23':11,'P1-24':8,'P1-26':7,
                'P1-29':5,'P1-31':6,'P1-32':12,'P1-33':13,'P1-35':19,'P1-36':16,'P1-37':26,'P1-38':20,'P1-40':21}


# pins 3 and 5 have permanent 1.8k pull ups to 3.3 volts 
PULLMAP = {'up':True,'down':False,'none':None}
# 'up'   internal pullup resistor to 3.3 volts
# 'down' internal pullup resistor to 0 volts
#  'none'  internal pullup resistor disconnected


# list of pins configurations
pins=[]

def read_pins():
    print("\n1 = pressed, 0 volts, 0 = not pressed, +3.3 volts")
    for pin in pins:
        print("Pin ",pin['board-name'],pin['GPIO-name'],pin['pin-object'].value)

for pin_def in PINLIST:
    pin={}
    try:
        pin_object=Button(BOARDMAP[pin_def],pull_up=PULLMAP['up'])

    except Exception as e:
        print ('GPIOZero Error:',e)
    else:
        pin['board-name']=pin_def
        pin['GPIO-name']='GPIO'+str(BOARDMAP[pin_def])
        pin['pin-object']=pin_object
        pins.append(pin)

while True:
    read_pins()
    sleep (1)



