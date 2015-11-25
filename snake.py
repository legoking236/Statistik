##############################################################################
##                                    ##                                    ##
##   This was entirely Jacob's Idea   ##        Coded by Alex Probst        ##
##   But i'm sure it will be a        ##        Statistik v0.5.14           ##
##   Fantastic waste of time!         ##        (c)2015 Alex Probst         ##
##                                    ##                                    ##
##############################################################################

#                    /^\/^\            _________              __
#                  _|__|  O|          /   _____/ ____ _____  |  | __ ____
#         \/     /~     \_/ \         \_____  \ /    \\__  \ |  |/ // __ \
#          \____|__________/  \       /        \   |  \/ __ \|    <\  ___/
#                 \_______      \    /_______  /___|  (____  /__|_ \\___  >
#                         `\     \           \/     \/     \/     \/    \/
#                           |     |                  \
#                          /      /                    \
#                         /     /                       \\
#                       /      /                         \ \
#                      /     /                            \  \
#                    /     /             _----_            \   \
#                   /     /           _-~      ~-_         |   |
#                  (      (        _-~    _--_    ~-_     _/   |
#                   \      ~-____-~    _-~    ~-_    ~-_-~    /
#                     ~-_           _-~          ~-_       _-~
#                        ~--______-~                ~-___-~

import threading
from Queue import Queue
import time

class snake:
    def __init__(self, master, master_size=[640,640], ctrlLay=['w','a','s','d'], startSize=4):
        self.master = master
        self.master_size = master_size
        self.ctrlLay = ctrlLay
        self.startSize = startSize
        self.pieces = [piece('r', [self.master_size[0]/2, self.master_size[1]/2], self.master)]
        for num in range(0, self.startSize):
            self.pieces.append(piece('r', [(self.master_size[0]/2)+16*(num+1), self.master_size[1]/2], self.master))
        self.alive = False

        self.validDirs = ['w', 's', 'Up', 'Down']

        self.q = Queue(maxsize=0)

        self.master.create_text(self.master_size[0]/2,self.master_size[1]/2, text="Press [space] to start..")
        self.master.focus_set()
        self.master.bind("<space>", self.playGame)
    def keyPress(self, event):
        print repr(event.keysym)
        if repr(event.keysym) in self.validDirs:
            print "hi"
            if repr(event.keysym) == 'w' or repr(event.keysym) == 'Up':
                self.validDirs = ['a', 'd', 'Left', 'Right']
                self.pieces[1].direction = 'u'
            elif repr(event.keysym) == 'a' or repr(event.keysym) == 'Left':
                self.validDirs = ['w', 's', 'Up', 'Down']
                self.pieces[1].direction = 'l'
            elif repr(event.keysym) == 's' or repr(event.keysym) == 'Down':
                self.validDirs = ['a', 'd', 'Left', 'Right']
                self.pieces[1].direction = 'd'
            elif repr(event.keysym) == 'd' or repr(event.keysym) == 'Right':
                self.validDirs = ['w', 's', 'Up', 'Down']
                self.pieces[1].direction = 'r'
            else:
                print ":()"
        else:
            pass
    def playGame(self, event):
        self.master.delete("all")
        for piece in self.pieces:
            piece.drawPiece(self.master)
        self.alive = True
        self.master.bind("<w>", self.keyPress)
        self.master.bind("<a>", self.keyPress)
        self.master.bind("<s>", self.keyPress)
        self.master.bind("<d>", self.keyPress)
        self.master.bind("<Up>", self.keyPress)
        self.master.bind("<Left>", self.keyPress)
        self.master.bind("<Down>", self.keyPress)
        self.master.bind("<Right>", self.keyPress)
        runThread = threading.Thread(target=self.runGame, args=(self.master,))
        runThread.start()
    def runGame(self, thMast):
        while self.alive:
            for piece in self.pieces:
                piece.move(thMast)
                time.sleep(0.1)
    def endGame(self):
        pass
class piece:
    def __init__(self, direction, cords, master, size=[16,16]):
        self.direction = direction
        self.size = size
        self.x = cords[0]
        self.y = cords[1]
        self.master = master
    def drawPiece(self, master):
        master.create_rectangle(self.x-self.size[0]/2, self.y-self.size[1]/2, self.x+self.size[0]/2, self.y+self.size[1]/2, fill="red", outline="red")
    def move(self, mast):
        if self.direction == 'r':
            self.x+=1
        elif self.direction == 'l':
            self.x-=1
        elif self.direction == 'u':
            self.y-=1
        elif self.direction == 'd':
            self.y+=1
        else:
            pass
        self.drawPiece(mast)
class food:
    def __init__(self):
        pass
