from math import *
from functools import cache
import pygame, sys, random


class Inputs():
    def refresh():
        pygame.mouse.get_rel()
    def mouseDelta():
        delta = pygame.mouse.get_rel()
        return Vector2(delta[0],delta[1])

class Vector2():
    def asTuple(self):
        return (self.x,self.y)
    def __getitem__(self,index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
    def __str__(self):
        return f"{self.x},{self.y}"
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return Vector2(self.x+other.x,self.y+other.y)
    def __radd__(self,other):
        return Vector2(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return self+(-other)
    def __rsub__(self,other):
        return -self+other
    def __mul__(self,other):
        return Vector2(self.x*other,self.y*other)
    def __rmul__(self,other):
        return Vector2(self.x*other,self.y*other)
    def __truediv__(self,other):
        return self*(1/other)
    def __neg__(vec):
        return Vector2(-vec.x,-vec.y)
    def randomInUnitCircle():
        x = (random.random()-0.5)*2
        y = (random.random()-0.5)*2
        if x*x + y*y >= 1:
           return Vector2.randomInUnitCircle()
        return Vector2(x,y)
    def perp(self):
        return Vector2(-self.y,self.x)
    def toPolar(self):
        return abs(self),self.getAngle()
    def toCart(r,theta):
        return Vector2(r*cos(theta),r*sin(theta))
    def norm(self):
        r = abs(self)
        return Vector2(self.x/r,self.y/r)
    def __abs__(self):
        return sqrt(self.x*self.x+self.y*self.y)
    def mod(self):
        return sqrt(self.x*self.x+self.y*self.y)
    def getAngle(self):
        x = self.x
        y = self.y
        r = abs(self)
        if r == 0: #Can't have an angle without a length
            return 0    
        As = asin(y/r) #As for AngleSin
        #correction for 4 quadrants
        if  y/r >= 0: #if sin of positive
            if x/r >= 0: #if cos of positive
                return abs(As)
            return pi -abs(As)
        elif x/r >= 0: #if cos of positive
            return 2*pi -abs(As)
        return pi +abs(As) # must be tan of positive
    def dotProd(first,second):
        return first.x*second.x + first.y*second.y
    def angleBetween(first,second):
        return second.getAngle()-first.getAngle()
    def bounceAgainst(self,other):
        angle = 2*other.getAngle()+2*pi-self.getAngle()
        r = abs(self)
        v = Vector2.toCart(r,angle)
        return v

class Entity():
    def __init__(self,name,color,pos):
        self.name = name
        self.color = color
        self.pos = pos
    def draw(self):
        pygame.draw.circle(SCREEN,self.color,self.relativePos().asTuple(),1/SCALE)
    def vectorTo(self,other):
        return other.pos - self.pos
    def directionTo(self,other):
        return self.vectorTo(other).norm()
    def distanceTo(self,other):
        return abs(self.distanceTo(other))
    def relativePos(self):
        return ORIGIN + (self.pos + OFFSET)/SCALE

class PhysicsEntity(Entity):
    def __init__(self, name, color, pos, vel, mass):
        super().__init__(name, color, pos)
        self.vel = vel
        self.mass = mass
    def precalc(self,others):
        for ent in others:
            self.calcForce
    def applycalc(self):
        self.updatePos()
        self.draw()
    def updatePos(self):
        self.pos += self.vel*deltaTime
    def calcAcc(self,force):
        self.preAcc = force/self.mass
    def calcVel(self):
        self.preVel += self.preAcc * deltaTime
    def applyForce(self,force):
        acc = force/self.mass
        self.vel += acc*deltaTime
    def forceDueToGravity(self,other):
        dist = self.distanceTo(other)
        mag = (self.mass*other.mass*G_CONSTANT)/(dist*dist)
        return self.directionTo(other)*mag
        

class PhysicsCircle(PhysicsEntity):
    def __init__(self, name, color, pos, vel, mass, radius):
        super().__init__(name, color, pos, vel, mass)
        self.radius = radius
    def draw(self):
        pygame.draw.circle(SCREEN,self.color,self.relativePos().asTuple(),self.radius/SCALE)

pygame.init()

SCREEN = None
CLOCK = None
FPS = 60
deltaTime = 1/FPS
ORIGIN = Vector2(0,0)
OFFSET = Vector2(0,0)
SCALE = 1

# Maths constants
G_CONSTANT = 6.67 * pow(10,-11)

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def start(dim):
    global SCREEN, ORIGIN, CLOCK
    SCREEN = pygame.display.set_mode(dim)
    pygame.display.set_caption("Space Simulator")
    ORIGIN = Vector2(dim[0]/2,dim[1]/2)
    CLOCK = pygame.time.Clock()

def main():
    global SCREEN, OFFSET, SCALE
    t = PhysicsCircle(1,WHITE,Vector2(0,0),Vector2(5,0),10,10)
    while True:
        SCREEN.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                 OFFSET += Inputs.mouseDelta()*SCALE
            if event.type == pygame.MOUSEWHEEL:
                m = -(event.y/10) + 1
                SCALE *= m

        pygame.display.flip()
        Inputs.refresh()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    start((400,400))
    main()
