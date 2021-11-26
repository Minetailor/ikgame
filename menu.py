from os import close
from tkinter import *
from tkinter.ttk import *
import gamespace
import leaderboardScript as l


def playGame():
    global mainCont
    closeMenu()
    m = gamespace.Main(root)
    if not(m.returnToMenu):
        mainCont = False
    openMenu()
    

def quitProgram():
    #Run quit program
    global mainCont
    mainCont = False

def openLeaderboard():
    closeMenu()
    a = l.Main(root)
    openMenu()

def closeMenu():
    backgroundImage.forget()
    playButton.forget()
    leaderboardButton.forget()
    quitButton.forget()


def openMenu():
    backgroundImage.pack()
    playButton.place(       relx=0.5, rely=0.4, anchor=CENTER)
    leaderboardButton.place(relx=0.5, rely=0.6, anchor=CENTER)
    quitButton.place(       relx=0.5, rely=0.8, anchor=CENTER)
    

def bossKey(event):
    global bossKeyToggle
    global c
    if bossKeyToggle:
        c.destroy()
        bossKeyToggle = False
    else:
        c = Canvas(root, width=1280, height=720)
        c.place(x=0,y=0,anchor=NW)
        boss = PhotoImage(file="bossKey.png")
        root.boss = boss
        c.create_image(0,0,image=root.boss, anchor=NW)        
        bossKeyToggle = True
    
bossKeyToggle = False
root = Tk()
root.protocol("WM_DELETE_WINDOW", quitProgram())
img = PhotoImage(file="placeholder.png")
backgroundImage = Label(image=img)

playButton = Button(root,text="PLAY",command=playGame)
leaderboardButton = Button(root,text="LEADERBOARD",command=openLeaderboard)
quitButton = Button(root,text="QUIT",command=quitProgram)

root.bind("b", bossKey)

openMenu()

height = root.winfo_height()
width = root.winfo_width()
root.update()

height = root.winfo_height()
width = root.winfo_width()

playButton.place(       relx=0.5, rely=0.4, anchor=CENTER)
leaderboardButton.place(relx=0.5, rely=0.6, anchor=CENTER)
quitButton.place(       relx=0.5, rely=0.8, anchor=CENTER)


root.resizable(False,False)


mainCont = True
while mainCont:

    root.update()