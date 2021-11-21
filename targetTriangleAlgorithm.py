from tkinter import *
import math
import time

class Vector2:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def set(self,newx,newy):
        self.x = newx
        self.y = newy

    def normalise(self):
        mag = self.magnitude()
        self.x = self.x/mag
        self.y = self.y/mag

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __add__(self,other):
        return Vector2(self.x+other.x,self.y+other.y)

    def __add__(self,other):
        return Vector2(self.x+other.x,self.y+other.y)

    def __sub__(self,other):
        return Vector2(self.x-other.x,self.y-other.y)

    def __isub__(self,other):
        return Vector2(self.x-other.x,self.y-other.y)

    def __mul__(self,n):
        return Vector2(self.x*n,self.y*n)

    def __str__(self):
        return str(self.x) + " " + str(self.y)

class Area:
    def __init__(self,root,width,height):
        self.root = root
        self.width = width
        self.height = height
        self.canvas = Canvas(root,width=width,height=height,background="white")
        self.canvas.pack()
        self.deltaTime = 0
        self.preTime = time.time()

    def calcDeltaTime(self):
        curTime = time.time()
        self.deltaTime = curTime - self.preTime
        self.preTime = curTime

class Joint:
    def __init__(self,position,length,angle=-(math.pi/2)):
        self.position = position
        self.angle = angle
        self.length = length

class Tentacle:
    def __init__(self,joints,area):
        self.joints = joints
        self.area = area
        self.numJoints = len(self.joints)
        self.end = joints[-1].position
        self.validDistance = 1
        self.setJoints()
        self.tentacle = self.area.canvas.create_line(self.jointPositions, width = 4, smooth=True)


    def setJoints(self):
        self.jointPositions = []
        for jointId in range(len(self.joints)-1):
            self.joints[jointId+1].position = self.joints[jointId].position + Vector2(math.cos(self.joints[jointId].angle)*self.joints[jointId].length,math.sin(self.joints[jointId].angle)*self.joints[jointId].length)
            self.jointPositions.append([self.joints[jointId].position.x,self.joints[jointId].position.y])
        self.jointPositions.append([self.joints[-1].position.x,self.joints[-1].position.y])
        self.end = self.joints[-1].position
    
    def update(self):
        self.setJoints()
        self.area.canvas.delete(self.tentacle)
        self.tentacle = self.area.canvas.create_line(self.jointPositions, width = 4, smooth=True)

    def follow(self,target):
        finalJoint = self.joints[-1]
        #self.end.set(finalJoint.position.x + math.cos(finalJoint.angle)*finalJoint.length, finalJoint.position.y + math.sin(finalJoint.angle)*finalJoint.length)
        self.end.set(finalJoint.position.x, finalJoint.position.y)

        a = (target-self.end)
        jid = self.numJoints-1

        timesRep = 0
        
        while a.magnitude() > self.validDistance and timesRep < 5:
            j = self.joints[jid]
            jtoe = self.end-j.position
            jtot = target-j.position
            etMag = jtoe.magnitude()*jtot.magnitude()
            if etMag <= 0.000001: # avoid small division/div by 0
                cosRot = 1
                sinRot = 0
            else:
                cosRot = (jtoe.x*jtot.x + jtot.y*jtoe.y) / etMag
                sinRot = (jtoe.x*jtot.y - jtoe.y*jtot.x) / etMag
            
            rotAng = math.acos(max(-1,min(1,cosRot)))

            rotAng = min(rotAng,math.pi*self.area.deltaTime)

            if sinRot < 0:
                rotAng = -rotAng
            
            self.setJoints()
            self.end = self.joints[-1].position
            j.angle += rotAng

            a = (target-self.end)
            if jid == 0:
                timesRep += 1
                self.setJoints()
                jid = self.numJoints
            jid -= 1

        

        

def quitProgram():
    global mainCont
    mainCont = False


root = Tk()
root.protocol("WM_DELETE_WINDOW", quitProgram)
mainArea = Area(root,800,800)
end = mainArea.canvas.create_line(0,0,0,0, width = 10, fill="red")

mousePos = Vector2(root.winfo_pointerx()-root.winfo_rootx(),root.winfo_pointery()-root.winfo_rooty())

js = [Joint(Vector2(300,300 + i*80),80, math.pi/2) for i in range(0,9)]

t = Tentacle(js,mainArea)

mainCont = True
while mainCont:
    mainArea.calcDeltaTime()
    root.update()
    mousePos.set(root.winfo_pointerx()-root.winfo_rootx(),root.winfo_pointery()-root.winfo_rooty())
    t.follow(mousePos)
    t.update()
    mainArea.canvas.coords(end,t.end.x,t.end.y,t.end.x,t.end.y+800)

