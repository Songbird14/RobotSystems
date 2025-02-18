#!/usr/bin/env python3

from picarx_improved import Picarx 
import Controls
import logging
import rossros as rr
px = Picarx()  


# ############# Part 1 
#initate the line following classes
sense = Controls.Sensing (px,False)
intperptret = Controls.Interpretation ()
drive = Controls.Controller(px)

#create functions for the ultrasonic sensor 
def get_ultrasonic_data ():
   distance = px.get_distance()
   print(f'ultrasonic={distance}')
   return distance

def process_ultrasonics(ul_data):
    threshold = 2
    if ul_data > threshold: 
        should_i_drive = 1
    else:
        should_i_drive = 2
    return should_i_drive
    
def drive_or_not(should_i_drive):
    if should_i_drive == 1:
         px.forward(25)
    elif should_i_drive == 2:
        px.forward(0)
    else:
        print('CONFUSED')

############ Part 2 - creeat buses and inital messages 
int_message1 = [1,2,3]
int_message2 = 0
bData = rr.Bus(int_message1,'Greyscale data bus')
bPosition = rr.Bus(int_message2,'Angle to drive bus')
bTerminate = rr.Bus(0, "Termination Bus")
bUltraData = rr.Bus(int_message2,"Ultrasonic Sensor data bus")
bUltraProcess = rr.Bus(int_message2,"Should I drive bus")


########### Part 3 -- create consumer/producer/ConsumerProducer
readData = rr.Producer(sense.greyscale,bData,0.1,bTerminate)
calculate_anlge = rr.ConsumerProducer(intperptret.processing,bData,bPosition,.1,bTerminate)
drivecar = rr.Consumer(drive.drive_along,bPosition,.1,bTerminate)

readUData = rr.Producer(get_ultrasonic_data,bUltraData,0.1,bTerminate)
calculate_shouldDrive = rr.ConsumerProducer(process_ultrasonics,bUltraData,bUltraProcess,.1,bTerminate)
stopcar = rr.Consumer(drive_or_not,bUltraProcess,.1,bTerminate)



######### Part 4 -- Create RossROS Printer and Timer objects 
terminationTimer = rr.Timer(bTerminate,5,0.1,bTerminate,"Termination Timer")

######### Part 5
producer_consumer_list = [readData,calculate_anlge,drivecar,readUData,calculate_shouldDrive,stopcar]
rr.runConcurrently(producer_consumer_list)




