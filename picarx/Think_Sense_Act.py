#!/usr/bin/env python3

from picarx_improved import Picarx
import Controls

class bus():
    message = 0 #message attribute 

    @classmethod 
    def write_message (cls): #write method
        passed_message = bus.message

    @classmethod 
    def read_message(cls): #read method
        return bus.message  ## is that what this line is supposed to do???
    
bus = bus() #create instance of class
delay = 1 #delay time

def producer(bus,delay):
        pass
        #while    what is supposed to end this while loop

def consumer_producer(bus,delay):
        pass
        #while    what is supposed to end this while loop 

def consumer(bus,delay):
        pass
        #while    what is supposed to end this while loop 