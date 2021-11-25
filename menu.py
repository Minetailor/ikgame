from tkinter import *
from tkinter.ttk import *
import gamespace


def playGame():
    global mainCont
    m = gamespace.Main(root)
    if not(m.returnToMenu):
        mainCont = False
    

def quitProgram():
    #Run quit program
    global mainCont
    mainCont = False

def openLeaderboard():
    print("leaderboard open")


root = Tk()
root.protocol("WM_DELETE_WINDOW", quitProgram())
img = PhotoImage(file="placeholder.png")
backgroundImage = Label(image=img)
backgroundImage.pack()
playButton = Button(root,text="PLAY",command=playGame)
leaderboardButton = Button(root,text="LEADERBOARD",command=openLeaderboard)
quitButton = Button(root,text="QUIT",command=quitProgram)

height = root.winfo_height()
width = root.winfo_width()
root.update()

height = root.winfo_height()
width = root.winfo_width()
print(width,height)

playButton.place(       relx=0.5, rely=0.4, anchor=CENTER)
leaderboardButton.place(relx=0.5, rely=0.6, anchor=CENTER)
quitButton.place(       relx=0.5, rely=0.8, anchor=CENTER)



mainCont = True
while mainCont:

    root.update()