from tkinter import *
from tkinter.ttk import *
import math


class Main: ## MAIN LEADERBOARD SCREEN
    def __init__(self, root):
        self.root = root
        self.height = root.winfo_height()
        self.width = root.winfo_width()

        self.leaderboard = Leaderboard()

        self.leaderBoardCanvas = Canvas(self.root,width=self.width,height=self.height)
        self.title = self.leaderBoardCanvas.create_text(self.width/2,0,anchor=N,text="LEADERBOARD")

        pos = 20
        self.text = [] ## Displays the leaderboard content
        for i,item in enumerate(self.leaderboard.board):
            disp = str(i+1) + ". " + item[1] + " : " + str(item[0])
            self.text.append(self.leaderBoardCanvas.create_text(self.width/2,pos,anchor=N,text=disp))
            pos += 15

        self.leaderBoardCanvas.place(x=0,y=0,anchor=NW)

        self.leaveButton = Button(self.leaderBoardCanvas,text="RETURN",command=self.leave)

        self.leaveButton.place(x=self.width/2,y=self.height,anchor=S)

        self.mainCont = True

        self.mainloop()

    def mainloop(self):
        while self.mainCont:
            self.root.update()
        self.leaderBoardCanvas.destroy()

    def leave(self): # leaves the leaderboard main screen
        self.mainCont = False

class Viewport: # different way to view the leaderboard, used at the end of the round.
    def __init__(self,frame,value):
        self.leaderboard = Leaderboard()
        self.frame = frame
        self.value = value

        self.height = 300
        self.width = 250
        print(self.height,self.width)

        self.canvas = Canvas(self.frame, width=self.width,height=self.height)

        n = math.floor(self.height/15)
        current = max(0,value-math.floor(n/2))

        #Displays only those immediately above and below
        
        pos = 0
        self.text = []
        for i in range(n):
            item = self.leaderboard.board[current]
            if current == value-1:
                disp = "===>"+ str(current+1) + ". " + item[1] + " : " + str(item[0]) + "<==="
            else:
                disp = str(current+1) + ". " + item[1] + " : " + str(item[0])
            self.text.append(self.canvas.create_text(self.width/2,pos,anchor=N,text=disp))
            pos += 15
            current += 1
            if current == len(self.leaderboard.board):
                break

        self.canvas.pack()





class Leaderboard: # holds everything to do with the leaderboard
    def __init__(self):
        self.fileName = "leaderboard.txt"
        file = open(self.fileName,"r")
        self.board = []
        for line in file:
            line = line.split()
            if len(line) != 0:
                self.board.append((int(line[0]),line[1]))

    def addItem(self,score,name): ##returns where the item was added. Adds the item into the ordered list
        pos = 0
        cont = True
        while cont and (pos != len(self.board)):
            if self.board[pos][0] < score:
                cont = False
            pos += 1
        
        a = self.board[:pos-1]
        b = self.board[pos-1:]
        a.append((score,name))
        a += b
        self.board = a
        return pos


    def write(self): # writes the new leaderboard to the leaderboard file
        leaderboardWrite = ""
        for item in self.board:
            leaderboardWrite += str(item[0]) + " " + item[1] + "\n"

        file = open(self.fileName, "w")
        file.write(leaderboardWrite)
        file.close()

