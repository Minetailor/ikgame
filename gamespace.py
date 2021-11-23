from tkinter import *
from tkinter.ttk import *
import math

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



class Main:
    def __init__(self,root): #give clean root
        self.parent = root
        self.height = root.winfo_height()
        self.width = root.winfo_width()
        self.root = Canvas(self.parent,width=self.width,height=self.height)
        self.root.place(x=0,y=0)

        self.root.bind("<Button-1>",self.clickevent)
        
        self.player = playerController(self,Vector2(self.width/2,self.height/2))
        self.items = []
        self.deltatime = 0.0
        self.makeItem()
        
        self.mainloop()

    def makeItem(self):
        i = Item(self,"placeholderItem.png",Vector2(0,0))
        self.items.append(i)

    def mainloop(self):
        global mainCont
        preTime = time.time()
        while mainCont:

            ## deltatime calcs
            curTime = time.time()
            self.deltatime = curTime - preTime
            preTime = curTime

            self.update()

            ## Item Hit Detection
            for item in self.items:
                dist = (self.player.pos-item.pos).magnitude()
                if dist < item.size+self.player.size:
                    print("blamo!")
            

    def update(self):
        for item in self.items:
            item.update()

        self.parent.update()

    def clickevent(self,event):
        for item in self.items:
            dist = (Vector2(event.x,event.y)-item.pos).magnitude()
            if dist < item.size:
                print("pop!")
        

class playerController:
    def __init__(self,mainArea,pos):
        self.pos = pos
        self.main = mainArea
        self.root = mainArea.root
        self.size = 10
        self.root.create_oval([self.pos.x-self.size,self.pos.y-self.size],[self.pos.x+self.size,self.pos.y+self.size])

class Item:
    def __init__(self, mainArea, imgPath, startpos, speed=50):
        self.main = mainArea
        self.root = mainArea.root
        self.imgPath = imgPath
        self.img = PhotoImage(file=imgPath)
        self.pos = startpos

        self.size = 20

        self.id = self.root.create_image(self.pos.x, self.pos.y, image=self.img)
        
        self.rotation = 0
        self.speed = speed
        self.direction = (self.main.player.pos-self.pos)
        self.direction.normalise()
        

    def update(self):
        diff = self.direction*self.speed*self.main.deltatime
        self.pos += diff
        self.root.move(self.id,diff.x,diff.y)
        
