#!/usr/bin/env python3

from picarx_improved import Picarx as px
import time
import logging
import cv2
from vilib import Vilib 
from PIL import Image 

class Sensing(): 
    def __init__(self, px, camera = False):
        self.px = px
        #self.px = Picarx()
        if camera: 
           print('in')
           Vilib.camera_start()
           time.sleep(0.2)
           self.path = "picarx"
           self.image_name = 'real_world' 
           self.px.set_cam_tilt_angle(-35)
           time.sleep(.2)

    def greyscale(self):
        data = self.px.grayscale.read()
        print (data)
        return data
    
    def camera(self):
        Vilib.take_photo(self.image_name, self.path)
        logging.info('photo taken')
        time.sleep(.1)
        return (self.image_name,self.path)
        

class Interpretation(): 
   def __init__(self, tolerance=.5, contrast = 1000): 
       self.tolerance = tolerance
       self.contrast = contrast  #1000 for desk #300 for guitar road 


   def processing(self, data):
    try:
        left = data[0]
        middle = data[1]
        right = data[2]

    except:
        position = 1

    try:
        data_norm=data
    
        normal = max(data)-min(data)
        left_norm=(data[0]-min(data))/normal
        middle_norm=(data[1]-min(data))/normal
        right_norm=(data[2]-min(data))/normal
    
        data_norm = [left_norm,middle_norm,right_norm]
        print(data_norm)
        print(f'normalized data = {data_norm}')
    except:
        position = 1
    
    try:

        if left > self.contrast and middle > self.contrast and right > self.contrast:
            print('LOST!')
            position = -2
        elif left_norm < self.tolerance and middle_norm > self.tolerance and right_norm > self.tolerance:
            print ('tape on left, turn left') #L,H,H
            position = -1
        elif left_norm < self.tolerance and middle_norm < self.tolerance and right_norm > self.tolerance:
            print ('tape on between left and center, turn slightly right') #L,L,H
            position = -.5
        elif left_norm > self.tolerance and middle_norm < self.tolerance and right_norm > self.tolerance:
                print('tape in the cetner, stay straight') #L,H,L
                position = 0    
        elif left_norm > self.tolerance and middle_norm < self.tolerance and right_norm < self.tolerance:
            print ('tape on between center and right, turn slightly left') #L,L,H
            position = .5 
        elif left_norm > self.tolerance and middle_norm > self.tolerance and right_norm < self.tolerance:
            print('tape on the right, turn left')
            position = 1
        else:
            print('In - but issue with the assigning position')
            position = 1
    except: 
        position = 1
    
    return position
    
   def photo_processing(self,image,path): 
        path = path
        image_name = image
        
        print('Started Processing')
        BnW = cv2.imread(f'{path}/{image_name}.jpg') #load image
        BnW  = BnW[375:450, :]
        _, width, _ = BnW.shape
        BnW = cv2.cvtColor(BnW,cv2.COLOR_BGR2GRAY) #convert to black and white

        #_,thresh = cv2.threshold(BnW,10,255,cv2.THRESH_BINARY_INV )
        thresh = cv2.Canny(BnW,30, 200)
        contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        cv2.drawContours(BnW,contours,-1,(0,255,0),3)
        #print("Number of Contours found = " + str(len(contours))) 
        cv2.imshow('Contours',BnW)
        cv2.waitKey(100)

        if (len(contours)) == 0:
            position = -2
            print('no_countours')
        else:
            tape = max(contours, key=cv2.contourArea)
            #print(tape)
            M = cv2.moments(tape)  #find the centroid of the tape 

        #get x,y coordinate of center 
            if M['m00'] != 0:
                cX = int(M["m10"] / M["m00"])
                position = (cX-(width/2))/(width/2)
            else:
                position = -2
                print('lost!')
    
       # cY = int(M["m01"] / M["m00"])
        return position 
       

class Controller():
    def __init__(self,px,P=30): 
        self.position = input
        self.P = P
        self.px = px
        self.px.forward(25)
        self.previous_angle = 0
    def drive_along(self,position):
        print('STARTED DRIVE FUNC')
        #self.px.forward(25)
        control = position*self.P
        if position != -2:
            self.px.set_dir_servo_angle(control)
            self.previous_angle = control
            print(f'angle = {control}')
        else:
            if self.previous_angle > 0:
                self.px.set_dir_servo_angle(35)
            elif self.previous_angle < 0:
                self.px.set_dir_servo_angle(-35)
            else:
                self.px.set_dir_servo_angle(0)
            print(f'angle = {self.previous_angle}')
        #return angle
        

def follow_the_line_greyscale():
   sensor = Sensing(False)
   think = Interpretation()
   angle = Controller()
   time.sleep(3)
   previous_angle = 0
   time_limit = 60
   time_out_start =time.time()
   sensor.px.forward(25)

   while time.time() != time_out_start+time_limit:
        data = sensor.greyscale()
        print(data)
        position = think.processing(data)
        print(position)
        contol = angle.drive_along(position)
        print(contol)
        if position != -2:
            sensor.px.set_dir_servo_angle(contol)
            previous_angle = contol
        else:
            if previous_angle > 0:
                sensor.px.set_dir_servo_angle(35)
            elif previous_angle < 0:
                sensor.px.set_dir_servo_angle(-35)
            else:
                sensor.px.set_dir_servo_angle(0)
        time.sleep(.25)

def follow_the_line_camera():
    sensor = Sensing(True)
    think = Interpretation()
    angle = Controller()
    time.sleep(3)
    previous_angle = 0

    time_limit = 60
    time_out_start =time.time()
    sensor.px.forward(25)
    while time.time() != time_out_start+time_limit:
        image = sensor.camera()
        position = think.photo_processing(image[0],image[1])
        contol = angle.drive_along(position)
        print(position)
        if position != -2:
            sensor.px.set_dir_servo_angle(contol)
            previous_angle = contol
        else:
            if previous_angle > 0:
                sensor.px.set_dir_servo_angle(35)
            elif previous_angle < 0:
                sensor.px.set_dir_servo_angle(-35)
            else:
                sensor.px.set_dir_servo_angle(0)
        time.sleep(.25)

if __name__== "__main__":
    val = input("Enter your choice of maneuver: ")
    val = int(val)
    if val == 1:
        follow_the_line_greyscale()

    elif val == 2: 
        follow_the_line_camera()
    else: 
        print('Invalid command. Try again')
