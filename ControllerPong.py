import random
import math
from nn import *

class ControllerPong():
    def __init__(self, w, h, dimPad, dimBall):
        
        self.__nn = nn(5,5,5,5)

        self.__posBall = [w // 2, h // 2]
        self.__posL = [10, h // 2]
        self.__posR = [w-10, h //2]
        self.__dimPad = dimPad
        self.__dimBall = dimBall
        self.__w = w
        self.__h = h
        self.__direction = 0

        self.__speed = 2
   
    def reset(self):
        self.__posBall = [self.__w // 2, self.__h // 2]
        self.__posL = [10, self.__h // 2]
        self.__posR = [self.__w - 10, self.__h // 2]

        self.__posBall[0] = self.__w // 2
        self.__posBall[1] = self.__h // 2
    
        self.__direction = random.randrange(-45,45)
	
        if random.randrange(2) == 0 :
            # Reverse ball direction, let the other guy get it first
            self.__direction += 180

        self.__speed = 2
    


    def update(self, numOfPlayers = 2):
        direction_radians = math.radians(self.__direction) 

        # Change the position (x and y) according to the speed and direction
        self.__posBall[1] += self.__speed * math.sin(direction_radians)
        self.__posBall[0] -= self.__speed * math.cos(direction_radians)


        if self.__posBall[1] < 10:
            self.__direction = (180-self.__direction)%360
            
        if self.__posBall[1] > self.__h - 10:
            self.__direction = (180-self.__direction)%360
            
    	
	
    #outside left   
        if self.__posBall[0] < 10:
            self.reset()
    #righr
        if self.__posBall[0] > self.__w - 10:
            self.reset()
    	
	
        if self.__posBall[0] <= 10:
            if self.__posBall[1] + self.__dimBall//2 >= self.__posL[1] and self.__posBall[1] + self.__dimBall//2 <= self.__posL[1] + self.__dimPad:
                self.__direction = (360-self.__direction)%360
	
	
        if self.__posBall[0] >= self.__w - 10:
            if self.__posBall[1] + self.__dimBall//2 >= self.__posR[1] and self.__posBall[1] + self.__dimBall//2 <=  self.__posR[1] + self.__dimPad:
                self.__direction = (360-self.__direction)%360
    		
		
    def learnL(self):
        pass
	
	
    def getBallPos(self):
        return self.__posBall
    def getPadPosL(self):
        return self.__posL
    def getPadPosR(self):
        return self.__posR

    def moveL(self, v):
        if self.__posL[1] - v // 3  > 20 and self.__posL[1] - v//3 < self.__h - 20 - self.__dimPad:
            self.__posL[1] -= v // 3
    
    def moveR(self, v):
        if self.__posR[1] - v // 3  > 20 and self.__posR[1] - v//3 < self.__h - 20 - self.__dimPad:
            self.__posR[1] -= v // 3









