#!/usr/bin/env python3

from picarx_improved import Picarx
import time

class Sensing(): 
    def __init__(self):
        self.px = Picarx()

    def greyscale(self):
        return self.px.grayscale.read()
   
class Interpretation(): 
   def __init__(self, tolerance= 500): 
       self.tolerance = tolerance

   def processing(self, data):
    left = data[0]
    middle = data[1]
    right = data[2]

    data_norm=data
    normal = max(data)-min(data)
    data_norm[0]=data[0]/normal
    data_norm[1]=data[1]/normal
    data_norm[2]=data[3]/normal
    
    data_norm = data
    print(data)
    diff_lm = data[0] - data[1]
    diff_mr = data[1] - data[2]

 

    if diff_lm < self.tolerance : 
        if left < middle:
            print ('tape on left, turn right') #L,H,H
            position = -1
        else:
            print ('tape on between left and center, turn slightly right') #L,L,H
            position = -.5
            
    elif diff_mr < self.tolerance:
        if right < middle: 
            print('tape on the right, turn left')
            position = 1
            
        else:
            print ('tape on between center and right, turn slightly left') #L,L,H
            position = .5
            
    elif (abs(diff_lm) - abs(diff_mr)) < self.tolerance: #H,L,H
        print('tape in the cetner, stay straight')
        position = 0
        
    else: 
        print('LOST!')
        position = -2

    return position
    

class Controller():
    def __init__(self,P=20): 
        self.position = input
        self.P = P
    def drive_along(self,input):
        angle = input*self.P
        return angle

def follow_the_line():
    time.sleep(2)
    sensor = Sensing()
    think = Interpretation()
   #angle = Controller()
    #px = Picarx()

    time_limit = 60
    time_out_start =time.time()

    while time.time() != time_out_start+time_limit:
        data = sensor.greyscale()
        print(data)
        position = think.processing(data)
        print(position)
        # contol = angle.drive_along(position)
        # if position != -2:
        #     px.forward(10,contol)
        # else:
        #     px.backward(10,0)
        time.sleep(1)


if __name__== "__main__":
    follow_the_line()
