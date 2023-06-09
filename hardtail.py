# Define Hardtail Class
# it occurs to me the kinematic calculations will be qualitatively
# different for the different suspension platforms so 
# i'll be doing a different class for each type of suspension

# 6/8/23: Drew the three easy tubes, got the dX and dY working well
# also drew the two wheels

# TODO
# Geometry to figure out the virtual line of the seat tube
# pin that line at the down-tube, constrain by seat tube length
# Draw the seat tube

import math
import cv2
import numpy as np

class Hardtail:
    # define default attributes, in this case Geometry
    # Starting with a hardtail, with our origin at the bottom bracket 
    # since that seems to be the convention
    WheelDiam = 740 # Wheel Diameter in mm
    FTravel = 160 # Front Travel in mm

    Stack = 648 # stack in mm
    Reach = 490 # reach in mm
    EffTT = 648 # Effective Top Tube in mm, measured from top of 
    # head tube to where it intersects the seat tube
    HTLength = 115 # head tube length in mm
    WheelBase = 1251 # wheelbase in mm
    BBDrop = 50.8 # BB Drop in mm
    CSLength = 420 # Chainstay Length in mm
    STAngle = 76 # Seat Tube Angle in Degrees
    HTAngle = 64 # Head tube angle in degrees
    a2c = 571 # axle to crown in mm

    # computed geometry
    # rear Axle position
    RAx = CSLength*-1
    RAy = BBDrop
    
    def draw(self):
        # draw a picture of the bike
        
        width = int(self.WheelDiam+self.WheelBase+200)
        ht = int(self.WheelDiam/2+self.Stack+200)
        canvas = np.zeros((ht, width, 3), dtype=np.uint8)
        # origin is in the top left because computers hate fun
        # gonna put together some offset variables because 
        # using the bike origin as the canvas origin leads to 
        # more than half the car being off the page 
        
        dX = 50+self.WheelDiam/2+self.CSLength
        print("dx",dX)
        dY = 50+self.WheelDiam/2

        
        # Compute the bottom of the head tube position
        HTRadians = math.radians(self.HTAngle)
        HTx = self.Reach + self.HTLength*math.cos(HTRadians)
        HTy = self.Stack - self.HTLength*math.sin(HTRadians)
        print("Reach",self.Reach)
        print("HTx", HTx)

        print("Stack",self.Stack)
        print("HTy",HTy)

        # Draw the head tube
        start_point = (int(self.Reach+dX), int(ht-self.Stack-dY))
        end_point = (int(HTx+dX), int(ht-HTy-dY))
        color = (255, 0, 0)
        thickness = 2

        cv2.line(canvas, start_point, end_point, color, thickness)

        # Draw the downtube
        start_point = end_point #downtube starts at the headtube
        end_point = (int(dX),int(ht-dY)) # the downtube connects to the
        # headtube from the bottom of the headtube to the bottom bracket, 
        # which is at 0,0
        cv2.line(canvas, start_point, end_point, color, thickness)
       
        # Draw the chainstay
        # compute the position of the rear axle
        
        start_point = end_point #chainstay starts at the bottom bracket
        end_point = (int(self.RAx+dX),int(ht-self.RAy-dY))
        cv2.line(canvas, start_point, end_point, color, thickness)
    
       

        #draw the rear wheel
        color = (255,255,255)
        center = (int(self.RAx+dX),int(ht-self.RAy-dY))
        radius = int(self.WheelDiam/2)
        cv2.circle(canvas, center, radius, color, thickness)

        #draw the front wheel
        center = (int(self.RAx+self.WheelBase+dX),int(ht-self.RAy-dY))
        cv2.circle(canvas, center, radius, color, thickness)

        cv2.imshow("Canvas", canvas)

        # this pair of lines closes the window when you press a key

        cv2.waitKey(0)
        cv2.destroyAllWindows() 

    