from tkinter import *
from tkinter.ttk import *
import math
import random
import leaderboardScript as l
import time

mainCont = True


class Vector2: # simple vector object

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def set(self,newx,newy):
        self.x = newx
        self.y = newy

    def normalise(self): # sets the vector to a magnitude of 1
        mag = self.magnitude()
        self.x = self.x/mag
        self.y = self.y/mag

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

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

### MAIN GAME CLASS ###
class Main:
    def __init__(self,root): 
        self.parent = root # parent root
        self.height = root.winfo_height()
        self.width = root.winfo_width()

        self.root = Canvas(self.parent,width=self.width,height=self.height) # canvas for main gameplay
        self.root.place(x=0,y=0)

        self.spawnCircle = max(self.width/2,self.height/2) # circle on which the items can spawn

        self.score = 0
        self.scoreTextID = self.root.create_text(0,0, text="Score: 0", anchor=NW)
        self.player = playerController(self,Vector2(self.width/2,self.height/2))
        self.lifeTextID = self.root.create_text(self.width,0, text="Lives: 3",anchor=NE)
        self.remainingTextID = self.root.create_text(self.width/2,0,text="Remaining: 1", anchor=N)

        self.bindKeys()
        
        self.mousePos = Vector2(0,0)
        i = Item(self,"coin.png",Vector2(-100,-100),speed=0) ## Odd workaround for ghost images appearing
        i.spawn()

        self.items = [i]
        self.deltatime = 0.0
        self.difficulty = 0.3
        self.remaining = 0

        self.waveTimer = 0
        self.waveNumber = 1
        self.wave = [[0.1,Item(self,"coin.png",Vector2(self.width/2,-50))]] # the 1st wave will always be this
        self.remaining = 1

        self.notPaused = True
        self.gameCont = True
        self.returnToMenu = False

        self.previousCombo = time.time()

        file = open("saveFile.txt","r") ## Checks to see if there is an ongoing save and loads that
        a = file.read(1)
        if a != "N":
            v = file.readlines()
            self.waveNumber = int(a+v[0])
            self.difficulty = float(v[1])
            self.decreaseLife(3-int(v[2]))
            self.increaseScore(int(v[3]))
            self.player.tentacle.deleteTentacle()
            self.player.setTentacle(Tentacle(self,self.player.pos,"purple",segLength=float(v[4])))
            self.generateWave()

        
        
        self.mainloop()

    def saveGame(self): # saves the game
        file = open("saveFile.txt","w")
        out =  str(self.waveNumber+1) + "\n"
        out += str(self.difficulty+0.1) + "\n"
        out += str(self.player.lives) + "\n"
        out += str(self.score) + "\n"
        out += str(self.player.tentacle.segLength)
        file.write(out)
        file.close()

    def debug_makeWave(self,event): # changes the current wave to a freshly generated one. DOES NOT delete items already in gamespace
        self.generateWave() 

    def debug_nextBuy(self,event): # moves the wave to the next buy phase. changes difficulty appropriately
        b = self.waveNumber % 5
        self.waveNumber += 5-b
        self.difficulty += 0.1*(5-b)

    def mainloop(self): # The main game loop is here
        preTime = time.time()
        while self.gameCont:

            ## Calculations for the change in time between frames
            curTime = time.time()
            self.deltatime = curTime - preTime
            preTime = curTime

            if self.notPaused:

                self.mousePos.set(self.parent.winfo_pointerx()-self.parent.winfo_rootx(),self.parent.winfo_pointery()-self.parent.winfo_rooty()) # gets mouse position
                self.player.tentacle.follow(self.mousePos)
                self.player.update()

                self.waveTimer += self.deltatime
                self.waveUpdate()

                ## Hit detection for the player. See if any items come in contact with the "body"
                for item in self.items:
                    item.update()
                    dist = (self.player.pos-item.pos).magnitude()
                    if dist < item.size+self.player.size:
                        self.decreaseLife(1)
                        self.items.remove(item)
                        self.remaining -= 1
                        self.player.hit = True
                        self.player.startHit = time.time()

                #updates the wave and items left in the wave counters
                self.root.itemconfigure(self.remainingTextID,text=("Wave: " + str(self.waveNumber) + "\nRemaining: "+ str(self.remaining)))
                
                if self.remaining == 0: # when the wave is over moves on to the next wave
                    if self.waveNumber % 5 == 0: #if the wave is a multiple of 5 takes you to the shop
                        self.shop()
                        self.saveGame() # saves once visted the shop
                    self.waveNumber += 1
                    self.difficulty += 0.1
                    self.generateWave()

            self.parent.update()
            self.parent.update_idletasks()
        self.root.destroy()

    def shop(self): # shop to claim upgrades
        self.pause()
        shopFrame = Frame(self.root,width=self.width/3,height=self.height/3)
        shopFrame.place(relx=0.5,rely=0.5, anchor=CENTER)
        
        lifeIncreaseB = Button(shopFrame, text="LIFE ++", command=self.shopLifeIncrease)
        lengthIncreaseB = Button(shopFrame, text="LENGTH ++", command=self.shopLengthIncrease)
        cooldownDecreaseB = Button(shopFrame, text="COOLDOWN --", command=self.shopReduceCooldown)

        lifeIncreaseB.place(relx=0.25,rely=0.5,anchor=CENTER)
        lengthIncreaseB.place(relx=0.75,rely=0.5,anchor=CENTER)
        cooldownDecreaseB.place(relx=0.5,rely=0.5,anchor=CENTER)

        self.unselected = True
        while self.unselected: # just a loop in the shop until it an option is chosen
            self.parent.update()

        shopFrame.destroy()

        self.resumeRound()


    def shopLengthIncrease(self): # Increase the length of the tentacle by 80.
        totalLength = self.player.tentacle.getTotalLength()
        totalLength += 80
        totalLength /= 4
        self.player.tentacle.deleteTentacle()
        self.player.setTentacle(Tentacle(self,self.player.pos,"purple",segLength=totalLength))
        self.unselected = False

    def shopReduceCooldown(self):
        if self.player.cooldown > 0:
            self.player.cooldown -= 0.2
        self.unselected = False

    def shopLifeIncrease(self): # increases the number of lives by 2
        self.decreaseLife(-2)
        self.unselected = False
    
    def lose(self): # when the game is over
        self.pause()
        file = open("saveFile.txt","w")
        file.write("N") # sets the save file to a NULL point
        file.close()

        s = Style(self.parent)
        s.configure("TFrame", background="red",relief=SUNKEN)

        f = Frame(self.parent,height=500,width=400,borderwidth=10)
        f.place(x=self.width/2,y=self.height/2,anchor=CENTER)
        t = Label(f,text="GAME OVER!!")
        t2 = Label(f,text="FINAL SCORE: "+str(self.score))
        t3 = Label(f,text="\/NAME\/")
        self.name_var = StringVar()
        e = Entry(f,textvariable=self.name_var) # Allows for entry of a name to be used in the leaderboard
        b1 = Button(f,text="MAIN MENU", command=self.returnMenuFromLoss)
        b2 = Button(f,text="SUBMIT SCORE",command=self.submit)

        e.place(relx=0.5, rely=0.5, anchor=CENTER)
        b2.place(relx=0.5,rely=0.6, anchor=CENTER)
        b1.place(relx=0.5,rely=0.9, anchor=CENTER)
        t.place(relx=0.5,rely=0.05, anchor=N)
        t2.place(relx=0.5,rely=0.15, anchor=CENTER)
        t3.place(relx=0.5,rely=0.45, anchor=CENTER)

        #used to keep track of widgets cleanly rather than many variables
        self.LosesGameWidgets = {
            "Frame" : f,
            "Title" : t,
            "Name"  : t3,
            "Entry" : e,
            "Submit": b2,
            "Play"  : b1,
            "Frame2": None
        }

    def returnMenuFromLoss(self): # returns to the main menu from a game over state
        self.gameCont = False
        self.LosesGameWidgets["Frame"].destroy()
        if self.LosesGameWidgets["Frame2"] != None:
            self.LosesGameWidgets["Frame2"].destroy()
        self.unbindKeys()
        self.returnToMenu = True

    def submit(self): # updates the leaderboard with your score
        n = self.name_var.get()
        self.LosesGameWidgets["Submit"].forget()
        a = l.Leaderboard()
        pos = a.addItem(self.score,n)
        a.write()
        self.LosesGameWidgets["Frame2"] = Frame(self.parent,height = 300,width = 250)
        self.LosesGameWidgets["Frame2"].place(relx=0.5,rely=0.5, anchor=CENTER)
        l.Viewport(self.LosesGameWidgets["Frame2"],pos)


    def pauseBinding(self,event): # method to open the pause menu
        self.pause()
        self.parent.bind("<Escape>", self.resumeBinding)

        pBackground = Style()
        pBackground.configure("TFrame",background="green")

        pauseMenu = Frame(self.parent, width=self.width/8,height=self.height/4)
        pauseMenu.place(relx=0.5,rely=0.5, anchor="center")
        resumeButton = Button(pauseMenu, text="RESUME",command=self.resume)
        resumeButton.place(relx=0.5, rely=0.2,anchor="center")
        menuButton = Button(pauseMenu, text="QUIT", command=self.returnMenu)
        menuButton.place(relx=0.5, rely=0.7, anchor="center")

        self.pauseMenu = pauseMenu

    def combo(self,event): # combo function for cheat code. P P P - increases life by 10
        current = time.time()
        if current-self.previousCombo < 1:
            self.comboCount += 1
            if self.comboCount == 3:
                self.decreaseLife(-10)
        else:
            self.comboCount = 1

        self.previousCombo = current

    
    def resumeBinding(self,event): # resumes the game after pause
        self.resume()

    def debug_boss(self,event): # used to do boss key while in the game.
        self.pause() # Pauses the game while in boss mode
        self.root.bind("b",self.debug_resume)

    def debug_resume(self,event): # used to do boss key while in the game
        self.root.unbind("b",self.debug_resume)
        self.bindKeys()
        self.notPaused = True

    def pause(self): # pauses the game
        self.unbindKeys()
        self.notPaused = False

    def resumeRound(self): # resumes the game
        self.bindKeys()
        self.notPaused = True

    def resume(self): # resumes the game from the pause menu
        self.bindKeys()
        self.notPaused = True
        self.pauseMenu.destroy()

    def unbindKeys(self): # unbinds all from in the gamespace
        self.parent.unbind("<Button-1>")
        self.parent.unbind("<Escape>")
        self.parent.unbind("k")
        self.parent.unbind("p")
        

    def bindKeys(self): # binds everything that is wanted in the gamespace
        self.parent.bind("<Button-1>",self.clickevent)
        self.parent.bind("<Escape>", self.pauseBinding)
        self.parent.bind("k", self.debug_nextBuy)
        self.root.bind("b",self.debug_boss)
        self.parent.bind("p",self.combo)
        

    def returnMenu(self): # returns to the main menu from the pause menu
        self.gameCont = False
        self.unbindKeys()
        self.pauseMenu.destroy()
        self.returnToMenu = True

    def generateWave(self): # generates a wave that depends upon difficulty
        self.wave = []
        n = math.ceil(10**self.difficulty) #Exponential increase in enemies
        self.remaining = n
        tmin = 1/self.difficulty # minimum and maximum time between item spawns
        tmax = 3/self.difficulty
        speedmax = math.ceil(50+10*self.difficulty) # max speed an item can move at the difficulty
        for i in range(n):
            angle = random.uniform(-math.pi,math.pi)
            speed = random.randint(49,speedmax)
            pos = Vector2(math.cos(angle),math.sin(angle))*self.spawnCircle
            nextItem = [random.uniform(tmin,tmax),Item(self,"coin.png",pos+self.player.pos,speed)] # creates a list of the time between item spawn and the item being spawned
            self.wave.append(nextItem)

        self.waveTimer = 0

    def waveUpdate(self):
        if len(self.wave) == 0:
            return
        if self.waveTimer > self.wave[0][0]: # checks whether the time has gone over an item spawn time
            self.wave[0][1].spawn()
            self.items.append(self.wave[0][1])
            self.waveTimer -= self.wave[0][0]
            del self.wave[0]
            self.waveUpdate()

    def clickevent(self,event): 
        if self.player.clickAnimation: # allows for a cooldown between clicks
            return
        self.player.startClickAnimation()
        toremove = []
        for item in self.items:
            distPlayer = (self.player.pos-item.pos).magnitude()
            distClick = (self.player.tentacle.end-item.pos).magnitude()
            if distPlayer < self.player.grabAura+item.size and distClick < item.size: # if the item in the grab aura of the player and if the item is at the end of the tentacle
                self.increaseScore(10)
                self.root.delete(item)
                self.parent.update()
                toremove.append(item)
                missed = False
                self.remaining -= 1
            
        for i in toremove:
            self.items.remove(i)

    def decreaseLife(self,amount):
        self.player.lives -= amount
        self.root.itemconfigure(self.lifeTextID,text="Lives: "+str(self.player.lives)) # updates life counter on loss of life
        if self.player.lives == 0:
            self.lose()

    def increaseScore(self,nscore):
        self.score += nscore
        self.root.itemconfigure(self.scoreTextID,text="Score: "+str(self.score))



class playerController:
    def __init__(self,mainArea,pos):
        self.pos = pos
        self.main = mainArea
        self.root = mainArea.root
        self.size = 10
        self.body = self.root.create_oval([self.pos.x-self.size,self.pos.y-self.size],[self.pos.x+self.size,self.pos.y+self.size],fill="black") # the player "body"
        self.startClickAnimationWait = 1
        self.cooldown = 1
        self.clickAnimation = False
        self.setTentacle(Tentacle(self.main,self.pos,"purple"))
        self.lives = 3
        self.hovering = False
        self.startHit = 0
        self.hitFlashTime = 2
        self.hit = False

    def setTentacle(self,t): # allows the tentacle to be changed
        self.tentacle = t
        self.grabAura = self.tentacle.getTotalLength()

    def update(self):
        self.tentacle.update()
        
        if self.startClickAnimationWait < self.cooldown: # allows for the colour of the tentacle to change
            self.startClickAnimationWait += self.main.deltatime
        else:
            self.hovering = False
            for item in self.main.items: # checks if there are any items on the end of the tentacle and changes the colour of the tentacle to blue
                distPlayer = (self.pos-item.pos).magnitude()
                distClick = (self.tentacle.end-item.pos).magnitude()
                if distPlayer < self.grabAura+item.size and distClick < item.size:
                    self.hovering = True
            if self.hovering:
                self.tentacle.colour = "blue"
            else:
                self.tentacle.colour = "purple"
            self.clickAnimation = False

        if self.hit:
            self.root.delete(self.body)
            self.body = self.root.create_oval([self.pos.x-self.size,self.pos.y-self.size],[self.pos.x+self.size,self.pos.y+self.size],fill="red")
            if self.hitFlashTime + self.startHit < time.time():
                self.hit = False
                self.body = self.root.create_oval([self.pos.x-self.size,self.pos.y-self.size],[self.pos.x+self.size,self.pos.y+self.size],fill="black")


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

        self.size = 16

        self.rotation = 0
        self.speed = speed
        self.direction = (self.main.player.pos-self.pos)
        self.direction.normalise()

    def spawn(self): # draws the item
        self.id = self.root.create_image(self.pos.x, self.pos.y, image=self.img)
        

    def update(self):
        diff = self.direction*self.speed*self.main.deltatime # moves the item closer to the target position
        self.pos += diff
        self.root.move(self.id,diff.x,diff.y)
        




###INVERSE KINEMATICS FOR TENTACLE FOLLOW###

class Joint: # simple object to store joint data
    def __init__(self,position,length,angle=-(math.pi/2)):
        self.position = position
        self.angle = angle
        self.length = length

class Tentacle:
    def __init__(self,area,start,colour,numJoints=4,segLength=20):
        self.colour = colour
        self.segLength = segLength
        # Generator for the set joints. placing them in a downwards line one after the other
        self.joints = [Joint(Vector2(start.x,start.y + i*self.segLength),self.segLength, math.pi/2) for i in range(0,numJoints)]
        self.area = area
        self.numJoints = numJoints
        self.end = self.joints[-1].position
        self.validDistance = 1
        self.setJoints()
        
        self.makeTentacles()

    def deleteTentacle(self): # deletes the tentacle from the canvas
        for tentacle in self.tentacles:
            self.area.root.delete(tentacle)

    def getTotalLength(self):
        return self.segLength*(self.numJoints-1)
        

    def makeTentacles(self): # draws the lines between the joints
        self.tentacles = []
        for i in range(self.numJoints-1):
            self.tentacles.append(self.area.root.create_line(self.jointPositions[i],self.jointPositions[i+1],width = self.segLength/4-i*2,fill=self.colour))

    def setJoints(self): # generates the joint positions so that they are attached
        self.jointPositions = []
        for jointId in range(self.numJoints-1):
            self.joints[jointId+1].position = self.joints[jointId].position + Vector2(math.cos(self.joints[jointId].angle)*self.joints[jointId].length,math.sin(self.joints[jointId].angle)*self.joints[jointId].length)
            self.jointPositions.append([self.joints[jointId].position.x,self.joints[jointId].position.y])
        self.jointPositions.append([self.joints[-1].position.x,self.joints[-1].position.y])
        self.end = self.joints[-1].position
    
    def update(self):
        self.setJoints()
        
        for tentacle in self.tentacles:
            self.area.root.delete(tentacle) # deletes and redraws the tentacles every frame
        self.makeTentacles()

    def follow(self,target): ##IK##
        finalJoint = self.joints[-1]
        #self.end.set(finalJoint.position.x + math.cos(finalJoint.angle)*finalJoint.length, finalJoint.position.y + math.sin(finalJoint.angle)*finalJoint.length)
        self.end.set(finalJoint.position.x, finalJoint.position.y)

        a = (target-self.end) # vector from the end to the target
        jid = self.numJoints-1 # joint id

        timesRep = 0
        
        while a.magnitude() > self.validDistance and timesRep < 5: # repeats this 5 times to optimised the position
            j = self.joints[jid]
            jtoe = self.end-j.position # joint to the end
            jtot = target-j.position # joint to the target
            etMag = jtoe.magnitude()*jtot.magnitude()
            if etMag <= 0.000001: # avoid small division/div by 0
                cosRot = 1
                sinRot = 0
            else:
                cosRot = (jtoe.x*jtot.x + jtot.y*jtoe.y) / etMag
                sinRot = (jtoe.x*jtot.y - jtoe.y*jtot.x) / etMag
            
            # finds the angle which the joint must be rotated by to place the end onto the same line as the joint to the target

            rotAng = math.acos(max(-1,min(1,cosRot))) 

            rotAng = min(rotAng,math.pi*self.area.deltatime) # slows down the rotation, makes it smooth to look at
            # finds which way it should rotate
            if sinRot < 0:
                rotAng = -rotAng
            
            self.setJoints()
            self.end = self.joints[-1].position
            j.angle += rotAng

            a = (target-self.end)
            if jid == 0: # loops until optimal found, or until 5 repetitions have happened
                timesRep += 1
                self.setJoints()
                jid = self.numJoints
            jid -= 1