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
     
        self.__speed = [random.uniform(-3,-2),random.uniform(-1.5,-2)]
	
        if random.uniform(0,1) < 0.5:
            self.__speed[0] *= -1
		
        self.__score = [0, 0]
   
    def reset(self):
        self.__posBall = [self.__w // 2, self.__h // 2]
        self.__posL = [10, self.__h // 2]
        self.__posR = [self.__w - 10, self.__h // 2]

        self.__posBall[0] = self.__w // 2
        self.__posBall[1] = self.__h // 2
    
        self.__speed = [random.uniform(-3,-2),random.uniform(-1.5,-2)]
	
        if random.uniform(0,1) < 0.5:
            self.__speed[0] *= -1

        print(self.__score)


    def update(self, numOfPlayers = 2):

        self.__posBall[0] += self.__speed[0]
        self.__posBall[1] += self.__speed[1]
	
	# left   
        if self.__posBall[0] < 5:
            self.reset()
            self.__score[1] += 1
    	# righr
        if self.__posBall[0] > self.__w - 5:
            self.reset()	
            self.__score[0] += 1


	# up
        if self.__posBall[1] < 10:
            self.__speed[1] *= -1
            if self.__speed[0] < 0:
                self.__speed[0] -= 0.2
            else:
                 self.__speed[0] += 0.2
	# down
        if self.__posBall[1] > self.__h - 10:
            self.__speed[1] *= -1
            if self.__speed[0] < 0:
                self.__speed[0] -= 0.2
            else:
                 self.__speed[0] += 0.2
	

	# player left
        if self.__posBall[0] <= 10:
            if self.__posBall[1] + self.__dimBall//2 >= self.__posL[1] and self.__posBall[1] + self.__dimBall//2 <= self.__posL[1] + self.__dimPad:
                self.__speed[0] *= -1
	
	# player right
        if self.__posBall[0] >= self.__w - 10:
            if self.__posBall[1] + self.__dimBall//2 >= self.__posR[1] and self.__posBall[1] + self.__dimBall//2 <=  self.__posR[1] + self.__dimPad:
                self.__speed[0] *= -1
	
	
		
    def learnL(self):
        pass
	
	
    def getBallPos(self):
        return self.__posBall
    def getPadPosL(self):
        return self.__posL
    def getPadPosR(self):
        return self.__posR

    def getScore(self):
        return self.__score

    def moveL(self, v):
        if self.__posL[1] - v // 5  > 20 and self.__posL[1] - v//5 < self.__h - 20 - self.__dimPad:
            self.__posL[1] -= v // 5
    
    def moveR(self, v):
        if self.__posR[1] - v // 5  > 20 and self.__posR[1] - v//5 < self.__h - 20 - self.__dimPad:
            self.__posR[1] -= v // 5









