#!/usr/bin/env python3

from picarx_improved import Picarx
import time

class Sensing(): 
    def __init__(self):
        self.px = Picarx()

    def greyscale(self):
        return self.px.grayscale.read()
   
class Interpretation(): 
   def __init__(self, tolerance=.5 ): 
       self.tolerance = tolerance
       #self.tolerance_out = tolerance_out

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

    if left_norm < self.tolerance and middle_norm > self.tolerance and right_norm > self.tolerance:
        print ('tape on left, turn right') #L,H,H
        position = -1
    elif left_norm < self.tolerance and middle_norm < self.tolerance and right_norm > self.tolerance:
        print ('tape on between left and center, turn slightly right') #L,L,H
        position = -.5
    elif left_norm > self.tolerance and middle_norm < self.tolerance and right_norm > self.tolerance:
        print('tape in the cetner, stay straight')
        position = 0    
    elif left_norm > self.tolerance and middle_norm < self.tolerance and right_norm < self.tolerance:
        print ('tape on between center and right, turn slightly left') #L,L,H
        position = .5 
    elif left_norm > self.tolerance and middle_norm > self.tolerance and right_norm < self.tolerance:
        print('tape on the right, turn left')
        position = 1
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
    angle = Controller()
    #px = Picarx()

    time_limit = 60
    time_out_start =time.time()

    while time.time() != time_out_start+time_limit:
        data = sensor.greyscale()
        print(data)
        position = think.processing(data)
        print(position)
        contol = angle.drive_along(position)
        print(contol)
        if position != -2:
            px.forward(10,contol)
        # else:
        #     px.backward(10,0)
        time.sleep(.5)


if __name__== "__main__":
    follow_the_line()
