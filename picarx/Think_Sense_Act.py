#!/usr/bin/env python3

from picarx_improved import Picarx 
import Controls
from time import sleep
import concurrent.futures
from threading import Event
from readerwriterlock import rwlock




class bus():
    def __init__(self,message):
        self.lock = rwlock.RWLockWriteD()
        self.message = message #message attribute 

    #@classmethod 
    def write_message (self, message): #write method
        with self.lock.gen_wlock():
             self.message = message
        #passed_message = bus.message

    #@classmethod 
    def read_message(self): #read method
        with self.lock.gen_rlock():
             message = self.message
        return message  
    

def producer(bus,delay,camera,cls): #needs delay, #Sensing
        sensing = Controls.Sensing(camera,cls)
        data = [0,0,0]
        while True:
            data = sensing.greyscale() 
            #data = [1,2,3]
            bus.write_message(data)
            #print(data)
            sleep(delay)
       

def consumer_producer(bus_read,bus_write,delay):  #needs delay 
        interpret = Controls.Interpretation()
        position = 0
        print("STARTED")
        while True:
            try:
                data = bus_read.read_message()
                print(data)

                position = interpret.processing(data)
                print(position)

                bus_write.write_message(position)
                sleep(delay)
            except:
                 print("FAILED")
                 sleep(delay)
        
def consumer(bus,delay):
        control = Controls.Controller()
        px.forward(25)
        while True: 
            position = bus.read_message()
            angle = control.drive_along(position)

            if position != -2:
                px.set_dir_servo_angle(angle)
                previous_angle = angle
            else:
                if previous_angle > 0:
                    px.set_dir_servo_angle(35)
                elif previous_angle < 0:
                    px.set_dir_servo_angle(-35)
                else:
                    px.set_dir_servo_angle(0)
            sleep(delay)


#Define shutdown event
shutdown_event = Event()



if __name__ == '__main__':
    int_message1 = [0,0,0]
    int_message2 = 0
    sensor_data = bus(int_message1) #create instance of class
    get_position = bus(int_message2)

    sensor_delay = .1
    interp_delay = .1
    drive_delay = .1

    #add options to switch between versions

    px = Picarx()  #might need to be a bus  

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(producer, sensor_data,sensor_delay,False,px)
        eInterpreter = executor.submit(consumer_producer,sensor_data, get_position, interp_delay) 
        eDrive = executor.submit(consumer, get_position, drive_delay)

    eSensor.result()
    eInterpreter.result()
    eDrive.result()



