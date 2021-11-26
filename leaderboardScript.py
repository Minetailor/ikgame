from tkinter import *
from tkinter.ttk import *


class Main:
    def __init__(self, root):
        self.root = root
        self.height = root.winfo_height()
        self.width = root.winfo_width()

        print(self.height)
        self.leaderboard = Leaderboard()

        self.leaderBoardCanvas = Canvas(self.root,width=self.width,height=self.height)
        self.title = self.leaderBoardCanvas.create_text(self.width/2,0,anchor=N,text="LEADERBOARD")

        pos = 20
        self.text = []
        for i,item in enumerate(self.leaderboard.board):
            disp = str(i+1) + ". " + item[1] + " : " + str(item[0])
            self.text.append(self.leaderBoardCanvas.create_text(self.width/2,pos,anchor=N,text=disp))
            pos += 15

        self.leaderBoardCanvas.place(x=0,y=0,anchor=NW)

        self.leaveButton = Button(self.leaderBoardCanvas,text="RETURN",command=self.leave)

        self.leaveButton.place(x=self.width/2,y=self.height,anchor=S)

        self.mainCont = True

        self.mainloop()
        print("this changed anything?")

    def mainloop(self):
        while self.mainCont:
            self.root.update()
        self.leaderBoardCanvas.destroy()

    def leave(self):
        self.mainCont = False
        
        print("HEKO")



class Leaderboard:
    def __init__(self):
        self.fileName = "leaderboard.txt"
        file = open(self.fileName,"r")
        self.board = []
        for line in file:
            line = line.split()
            if len(line) != 0:
                self.board.append((int(line[0]),line[1]))

    def addItem(self,score,name):
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


    def write(self):
        leaderboardWrite = ""
        for item in self.board:
            leaderboardWrite += str(item[0]) + " " + item[1] + "\n"

        file = open(self.fileName, "w")
        file.write(leaderboardWrite)
        file.close()

