from random import randint
import time

class MyPerson:
    tracks = []
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        #print "array",self.tracks
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def going_UP(self,lineaUp):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < lineaUp and self.tracks[-2][1] >= lineaUp: #cruzo la linea [-1] primer elemento de der a izq [1] coord en y
                    state = '1'
                    self.dir = 'up'
                    print "ultimo?",self.tracks[-1][1]
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,lineaDown):
        if len(self.tracks) >= 2:
            if self.state == '0':

                if self.tracks[-1][1] > lineaDown and self.tracks[-2][1] <= lineaDown: #cruzo la linea
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
class MultiPerson:
    def __init__(self, persons, xi, yi):
        self.persons = persons
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
