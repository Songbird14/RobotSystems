#!/usr/bin/env python3

from picarx_improved import Picarx
import time
import cv2
from vilib import Vilib 

class Sensing(): 
    def __init__(self):
        self.px = Picarx()
        if camera: 
           Vilib.camera.start()
           time.sleep(0.5)
           self.path = 'picarx'
           self.image_name = 'image' 

    def greyscale(self):
        return self.px.grayscale.read()
    def camera(self):
        Vilib.take_photo(self.image_name, self.path)
   
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

def follow_the_line_camera(path, image_name):
    BnW = cv2.imread(f'{path}/{image_name}.jpg')
    BnW = cv2.cvtColor(BnW,cv2.COLOR_BGR2GRAY)
   # BnW = BnW[img_]


if __name__== "__main__":
    #follow_the_line_greyscale()
    Vilib.camera.start()
    time.sleep(0.5)
    Vilib.display()