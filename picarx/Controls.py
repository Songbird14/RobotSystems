#!/usr/bin/env python3

from picarx_improved import Picarx
import time
import logging
import cv2
from vilib import Vilib 

class Sensing(): 
    def __init__(self, camera):
        self.px = Picarx()
        if camera: 
           print('in')
           Vilib.camera_start()
           time.sleep(0.5)
           self.path = "picarx"
           self.image_name = 'real_world' 
           self.px.set_cam_tilt_angle(-35)
           time.sleep(.5)

    def greyscale(self):
        return self.px.grayscale.read()
    
    def camera(self):
        Vilib.take_photo(self.image_name, self.path)
        logging.debug('photo taken')
        time.sleep(.1)
        return self.image_name,self.path
        

class Interpretation(): 
   def __init__(self, tolerance=.5, contrast = 1000): 
       self.tolerance = tolerance
       self.contrast = contrast  #1000 for desk #300 for guitar road 


   def processing(self, data):
    left = data[0]
    middle = data[1]
    right = data[2]

    data_norm=data
    normal = max(data)-min(data)
    left_norm=(data[0]-min(data))/normal
    middle_norm=(data[1]-min(data))/normal
    right_norm=(data[2]-min(data))/normal
    
    data_norm = [left_norm,middle_norm,right_norm]
    print(data_norm)

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

    return position
    
   def photo_processing(self,image,path): 
        lower_limit =170
        upper_limit = 149
        path = path
        image_name = image
        
        print('Started Processing')
        BnW = cv2.imread(f'{path}/{image_name}.jpg') #load image
        BnW = cv2.cvtColor(BnW,cv2.COLOR_BGR2GRAY) #convert to black and white

        _,thresh = cv2.threshold(BnW,10,255,cv2.THRESH_BINARY_INV )
        # edges = cv2.Canny(BnW,lower_limit, upper_limit)
        contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        edged_image = cv2.drawContours(BnW,contours,-1,(0,255,0),3)

        cv2.imshow('Contours',BnW)
        cv2.waitKey(100)
        return edged_image


        # thresh = cv2.adaptiveThreshold(edges,255,1,1,11,2)
        # cv2.imshow('Real_world',BnW)

        

       

class Controller():
    def __init__(self,P=30): 
        self.position = input
        self.P = P
    def drive_along(self,input):
        angle = input*self.P
        return angle

def follow_the_line_greyscale():
    sensor = Sensing()
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
    #angle = Controller()
    #time.sleep(3)
    #previous_angle = 0
    image = sensor.camera()
    process = think.photo_processing(image[0],image[1])

if __name__== "__main__":
    follow_the_line_camera()
    #follow_the_line_greyscale()
   # Vilib.camera_start()
    #time.sleep(0.5)
    #Vilib.display()
