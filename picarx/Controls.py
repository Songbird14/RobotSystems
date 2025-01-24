#!/usr/bin/env python3

from picarx_improved import Picarx

class Sensing(): 
    def __init__(self):
        self.px = Picarx()

    def greyscale(self):
        return self.px.grayscale.read()
   
class Interpretation(): 
   def __init__(self, tolerance= 10): 
       self.px = Picarx()
       self.tolerance = tolerance

   def processing(self, data,):
    left = data[0]
    middle = data[1]
    right = data[2]
    diff_lm = data[0] - data[1]
    diff_mr = data[1] - data[2]

    #set up for returning speed, angles 
    self.speed = 0 
    self.angle = 0

    if diff_lm > self.tolerance : 
        if left < middle:
            print ('tape on left, turn right') #L,H,H
            #self.speed = 10
            #self.angle = 30
        else:
            print ('tape on between left and center, turn slightly right') #L,L,H
            #self.speed = 10
            #self.angle = 15
    elif diff_mr > self.tolerance:
        if right < middle: 
            print('tape on the right, turn left')
            #self.speed = 10
            #self.angle = -30
        else:
            print ('tape on between center and right, turn slightly left') #L,L,H
            #self.speed = 10
            #self.angle = -15
    elif (abs(diff_lm) - abs(diff_mr)) < self.tolerance: #H,L,H
        print('tape in the cetner, stay straight')
        #self.speed = 10
        #self.angle = 0
    else: 
        print('LOST!')
        #self.speed = 0
        #self.angle = 0

    return [self.speed, self.angle]
    
    #low equals darker 
    #if all high do the previous action 
    #normalize (take max and min)
    
class Controller():
    def __init__(self): 
        pass 
    def drive_along(self):
        pass

def follow_the_line():
    sensor = Sensing()
    think = Interpretation()
    drive = Controller()

if __name__== "__main__":
    follow_the_line()