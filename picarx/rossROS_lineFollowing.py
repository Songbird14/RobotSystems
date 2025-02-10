#!/usr/bin/env python3

from picarx_improved import Picarx 
import Controls
import logging
from RossROS import rossros as rr
px = Picarx()  #might need to be a bus  


############# Part 1 
def data(camera,cls): #needs delay, #Sensing
    sensing = Controls.Sensing(camera,cls)
    data = sensing.greyscale() 
    return data 

def process(data):  #needs delay 
    interpret = Controls.Interpretation()
    position = interpret.processing(data)
    return position
        
def drive(position):
    control = Controls.Controller()
    px.forward(25)
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

def get_ultrasonic_data ():
    return px.ultrasonic.read()

def process_ultrasonics(ul_data):
    if ul_data > 0: 
        should_i_drive = True
    else:
        should_i_drive = False
    
def drive_or_not(should_i_drive):
    if should_i_drive == True:
        px.forward(25)
    elif should_i_drive == False:
        px.forward(0)
    else:
        print('CONFUSED')


############ Part 2
int_message1 = [0,0,0]
int_message2 = 0
bData = rr.Bus(int_message1,'Greyscale data bus')
bPosition = rr.Bus(int_message2,'Angle to drive bus')
bTerminate = rr.Bus(0, "Termination Bus")


########### Part 3 -- create consumer/producer/ConsumerProducer
readData = rr.Producer(data(False,px),bData,0.1,bTerminate)
calculate_anlge = rr.ConsumerProducer(process,bData,bPosition,.1,bTerminate)
drivecar = rr.Consumer(drive,bPosition,.1,bTerminate)


######### Part 4 -- Create RossROS Printer and Timer objects 
terminationTimer = rr.Timer(bTerminate,5,0.1,bTerminate,"Termination Timer")

######### Part 5
producer_consumer_list = [readData,calculate_anlge,drivecar]

rr.runConcurrently(producer_consumer_list)




