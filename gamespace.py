from tkinter import *
from tkinter.ttk import *
import math
import random

import time

mainCont = True


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


def debug(event):
    print("WHAAAT")


class Main:
    def __init__(self,root): #give clean root
        self.parent = root
        self.height = root.winfo_height()
        self.width = root.winfo_width()
        self.root = Canvas(self.parent,width=self.width,height=self.height)



        self.spawnCircle = max(self.width/2,self.height/2)
        print(self.width,self.height)
        print(self.spawnCircle)

        self.score = 0
        self.scoreTextID = self.root.create_text(0,0, text="Score: 0", anchor=NW)

        

        self.root.place(x=0,y=0)

        self.bindKeys()
        
        
        self.player = playerController(self,Vector2(self.width/2,self.height/2))

        self.lifeTextID = self.root.create_text(self.width,0, text="Lives: 3",anchor=NE)

        self.mousePos = Vector2(0,0)
        i = Item(self,"placeholderItem.png",Vector2(-100,-100),speed=0) ## Odd workaround for ghost images appearing
        i.spawn()

        self.items = [i]
        self.deltatime = 0.0
        self.difficulty = 1

        self.waveTimer = 0
        self.wave = []

        self.notPaused = True
        self.gameCont = True
        self.returnToMenu = False
        
        self.mainloop()

    def debug_makeWave(self,event):
        print("spawwwn")
        self.generateWave()

    def makeItem(self):
        angle = random.uniform(0,math.pi*2)
        spc = self.spawnCircle + 10 ## currently for size, although size may not change
        i = Item(self,"placeholderItem.png",Vector2(math.cos(angle),math.sin(angle))*spc)
        self.items.append(i)

    def mainloop(self):
        preTime = time.time()
        while self.gameCont:

            ## deltatime calcs
            curTime = time.time()
            self.deltatime = curTime - preTime
            preTime = curTime

            if self.notPaused:

                self.mousePos.set(self.parent.winfo_pointerx()-self.parent.winfo_rootx(),self.parent.winfo_pointery()-self.parent.winfo_rooty())
                self.player.tentacle.follow(self.mousePos)
                self.player.update()

                self.waveTimer += self.deltatime
                self.waveUpdate()

                ## Item Hit Detection
                for item in self.items:
                    item.update()
                    dist = (self.player.pos-item.pos).magnitude()
                    if dist < item.size+self.player.size:
                        self.decreaseLife(1)
                        self.items.remove(item)
                        print("HIT!")

            self.parent.update()
            self.parent.update_idletasks()
        self.root.destroy()

    def pauseBinding(self,event):
        self.pause()
        self.parent.bind("<Escape>", self.resumeBinding)

        pBackground = Style()
        pBackground.configure("TFrame",background="green")

        pauseMenu = Frame(self.parent, width=self.width/4,height=self.height/2)
        pauseMenu.place(relx=0.5,rely=0.5, anchor="center")
        resumeButton = Button(pauseMenu, text="RESUME",command=self.resume)
        resumeButton.place(relx=0.5, rely=0.2,anchor="center")
        menuButton = Button(pauseMenu, text="QUIT", command=self.returnMenu)
        menuButton.place(relx=0.5, rely=0.7, anchor="center")

        self.pauseMenu = pauseMenu

    def resumeBinding(self,event):
        self.resume()
        


    def pause(self):
        self.unbindKeys()

        self.notPaused = False

    def resume(self):
        self.bindKeys()
        self.notPaused = True
        self.pauseMenu.destroy()

    def unbindKeys(self):
        self.parent.unbind("a")
        self.parent.unbind("<Button-1>")
        self.parent.unbind("<Escape>")

    def bindKeys(self):
        self.parent.bind("a",self.debug_makeWave)
        self.parent.bind("<Button-1>",self.clickevent)
        self.parent.bind("<Escape>", self.pauseBinding)

    def returnMenu(self):
        self.gameCont = False
        self.unbindKeys()
        self.pauseMenu.destroy()
        self.returnToMenu = True


    

    def generateWave(self):
        self.wave = []
        n = math.ceil(10**self.difficulty)
        tmin = 1/self.difficulty # too small
        tmax = 3/self.difficulty
        for i in range(n):
            angle = random.uniform(-math.pi,math.pi)
            pos = Vector2(math.cos(angle),math.sin(angle))*self.spawnCircle
            nextItem = [random.uniform(tmin,tmax),Item(self,"placeholderItem.png",pos+self.player.pos)]
            self.wave.append(nextItem)

        self.waveTimer = 0

    def waveUpdate(self):
        if len(self.wave) == 0:
            return
        if self.waveTimer > self.wave[0][0]:
            self.wave[0][1].spawn()
            self.items.append(self.wave[0][1])
            self.waveTimer -= self.wave[0][0]
            del self.wave[0]
            self.waveUpdate()

    def clickevent(self,event):
        if self.player.clickAnimation:
            return
        self.player.startClickAnimation()
        toremove = []
        for item in self.items:
            distPlayer = (self.player.pos-item.pos).magnitude()
            distClick = (Vector2(event.x,event.y)-item.pos).magnitude()
            if distPlayer < self.player.grabAura+item.size and distClick < item.size:
                self.increaseScore(10)
                self.root.delete(item)
                self.parent.update()
                toremove.append(item)
                missed = False
                print("pop!")
            
        for i in toremove:
            self.items.remove(i)

    def decreaseLife(self,amount):
        self.player.lives -= amount
        self.root.itemconfigure(self.lifeTextID,text="Lives: "+str(self.player.lives))

    def increaseScore(self,nscore):
        self.score += nscore
        self.root.itemconfigure(self.scoreTextID,text="Score: "+str(self.score))



class playerController:
    def __init__(self,mainArea,pos):
        self.pos = pos
        self.main = mainArea
        self.root = mainArea.root
        self.size = 10
        self.root.create_oval([self.pos.x-self.size,self.pos.y-self.size],[self.pos.x+self.size,self.pos.y+self.size])
        self.startClickAnimationWait = 1
        self.clickAnimation = False
        self.tentacle = Tentacle(self.main,self.pos,"purple")
        self.grabAura = self.tentacle.getTotalLength()
        self.lives = 3
        print(self.grabAura)

    def update(self):
        self.tentacle.update()
        if self.startClickAnimationWait < 1:
            self.startClickAnimationWait += self.main.deltatime
        else:
            self.tentacle.colour = "purple"
            self.clickAnimation = False

    def startClickAnimation(self):
        self.clickAnimation = True
        self.tentacle.colour = "red"
        self.startClickAnimationWait = 0

class Item:
    def __init__(self, mainArea, imgPath, startpos, speed=50):
        self.main = mainArea
        self.root = mainArea.root
        self.imgPath = imgPath
        self.img = PhotoImage(file=imgPath)
        self.pos = startpos

        self.size = 20

        self.rotation = 0
        self.speed = speed
        self.direction = (self.main.player.pos-self.pos)
        self.direction.normalise()

    def spawn(self):
        self.id = self.root.create_image(self.pos.x, self.pos.y, image=self.img)
        

    def update(self):
        diff = self.direction*self.speed*self.main.deltatime
        self.pos += diff
        self.root.move(self.id,diff.x,diff.y)
        




##INVERSE KINEMATICS FOR TENTACLE FOLLOW###

class Joint:
    def __init__(self,position,length,angle=-(math.pi/2)):
        self.position = position
        self.angle = angle
        self.length = length

class Tentacle:
    def __init__(self,area,start,colour,numJoints=4,segLength=20):
        self.colour = colour
        self.segLength = segLength
        self.joints = [Joint(Vector2(start.x,start.y + i*self.segLength),self.segLength, math.pi/2) for i in range(0,numJoints)]
        self.area = area
        self.numJoints = numJoints
        self.end = self.joints[-1].position
        self.validDistance = 1
        self.setJoints()
        
        self.makeTentacles()

    def getTotalLength(self):
        return self.segLength*(self.numJoints-1)
        

    def makeTentacles(self):
        self.tentacles = []
        for i in range(self.numJoints-1):
            self.tentacles.append(self.area.root.create_line(self.jointPositions[i],self.jointPositions[i+1],width = 5-i*2,fill=self.colour))

    def setJoints(self):
        self.jointPositions = []
        for jointId in range(self.numJoints-1):
            self.joints[jointId+1].position = self.joints[jointId].position + Vector2(math.cos(self.joints[jointId].angle)*self.joints[jointId].length,math.sin(self.joints[jointId].angle)*self.joints[jointId].length)
            self.jointPositions.append([self.joints[jointId].position.x,self.joints[jointId].position.y])
        self.jointPositions.append([self.joints[-1].position.x,self.joints[-1].position.y])
        self.end = self.joints[-1].position
    
    def update(self):
        self.setJoints()
        
        for tentacle in self.tentacles:
            self.area.root.delete(tentacle)
        self.makeTentacles()

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

            rotAng = min(rotAng,math.pi*self.area.deltatime)

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