#! /usr/bin/env python3

"""
!!!! THIS PROGRAM COULD DAMAGE YOUR PI IF GPIO IS NOT CORRECTLY CONNECTED
To Run - python3 output_test.py from a terminal window

Out of the box no outputs change state.
The commented out PINLIST = [......] statement is a list of all the pins that can be used by Pi Presents
Modify the uncommented PINLIST = [] to add the pins to be toggled.

Running the program will change the state of the selected pins every 2 seconds
A log will be written to the terminal window.
To exit type CTRL-C
 
"""
#PINLIST = ['P1-03','P1-05','P1-07','P1-08',
#                'P1-10','P1-11','P1-12','P1-13','P1-15','P1-16','P1-18','P1-19',
#                'P1-21','P1-22','P1-23','P1-24','P1-26']

#PINLIST = ['P1-03','P1-05','P1-07','P1-08',
                #'P1-10','P1-11','P1-12','P1-13','P1-15','P1-16','P1-18','P1-19',
                #'P1-21','P1-22','P1-23','P1-24','P1-26',
                #'P1-29','P1-31','P1-32','P1-33','P1-35','P1-36','P1-37','P1-38','P1-40']
                
PINLIST = []

                
BOARDMAP = {'P1-03':2,'P1-05':3,'P1-07':4,'P1-08':14,
               'P1-10':15,'P1-11':17,'P1-12':18,'P1-13':27,'P1-15':22,'P1-16':23,'P1-18':24,'P1-19':10,
               'P1-21':9,'P1-22':25,'P1-23':11,'P1-24':8,'P1-26':7,
                'P1-29':5,'P1-31':6,'P1-32':12,'P1-33':13,'P1-35':19,'P1-36':16,'P1-37':26,'P1-38':20,'P1-40':21}

#computed configuration of pins
pins=[]

import sys
if sys.version_info[0] != 3:
        sys.stdout.write("ERROR: Pi Presents requires python 3\nHint: python3 output_test.py .......\n")
        exit(102)

from gpiozero import DigitalOutputDevice,Button
from time import sleep


def write_pins(value):
    for pin in pins:
        print("Pin ",pin['board-name'],pin['GPIO-name'])
        pin['pin-object'].value=value


if PINLIST == []:
    print ('ERROR: No pins selected\nRead the instructions by opening output_test.py in an editor\n')
    exit()

for pin_def in PINLIST:
    pin={}
    try:
        pin_object=DigitalOutputDevice(BOARDMAP[pin_def])

    except Exception as e:
        print ('GPIOZero Error:',e)
    else:
        pin['board-name']=pin_def
        pin['GPIO-name']='GPIO'+str(BOARDMAP[pin_def])
        pin['pin-object']=pin_object
        pins.append(pin)

while True:
        print('\n***** ON = +3.3 volts ******')
        write_pins(1)
        sleep (2)
        print('\n***** OFF = 0 volts *****')
        write_pins(0)
        sleep(2)



