import time
from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self, p):
        try:
            memProxy= ALProxy("ALMemory", "localhost",9559) #change to 9559 when working on real pepper
        except RuntimeError, e:
            self.onError(e)
        self.onLeft=False
        self.onRight=False
        fringe=memProxy.getData("fringe") #get data from memory
        turn=memProxy.getData("turn")
        played=memProxy.getData("played")
        hand=memProxy.getData("hand")
        nb=memProxy.getData("tilesPlayer")
        dom=p[0] #dom is input
        if dom not in played: #if the domino is not played
            if dom not in hand: #if domino not in pepper's hand
                if dom[0] in range(7) and dom[1] in range(7): #if domino recognized
                    self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png") #show tablet
                    if dom[0]==dom[1]:
                        if dom[0]==0:
                            face="blank"
                        else:
                            face=str(dom[0])
                        say="You are playing the double " + face
                    else:
                        if dom[0]==0:
                            lface="blank"
                        else:
                            lface=str(dom[0])
                        if dom[1]==0:
                            rface="blank"
                        else:
                            rface=str(dom[1])
                        say='You are playing the domino %(left)s %(right)s' % {"left":lface, "right":rface} #feedback
                    flagChange=True #allow change (man...)
                    if (dom==fringe or dom==[fringe[1],fringe[0]]): #if there is an ambiguity
                        say=say+", but I don't know on which side of the game you are placing it. Please touch my left or right hand to indicate where you are placing it."
                        self.onSay(say)
                        self.onSelect() #use hand to select
                         #y tho?
                        while not (self.onLeft or self.onRight): #while the hand is not touched
                            pass #wait
                        if self.onLeft or self.onRight: #if the hand has been touched
                            if self.onLeft: #if the touch is touching left side of screen (dom[1])
                                side=dom[0]
                                if dom[0]==fringe[0]:
                                    fringe[0]=dom[1]
                                else:
                                    fringe[1]=dom[1]
                            elif self.onRight:
                                side=dom[1]
                                if dom[1]==fringe[0]:
                                    fringe[0]=dom[0]
                                else:
                                    fringe[1]=dom[0]
                            flagChange=False
                            say="you are placing it next to"+str(side)
                    else: #if the hand has not being touched
                        for i in [0,1]: #for each side of the fringe
                            for j in [0,1]: #for each side of the domino
                                if fringe[i]==dom[j] and flagChange: #if the domino can be placed and is allowed
                                    fringe[i]=dom[(j+1)%2] #add the other side of the domino to the fringe
                                    flagChange=False #refuse the change
                                    break

                    if flagChange: #if you don't know where to put the tile
                        say="I am affraid you cannot play that tile"
                        self.onAgain(say)
                         #say
                    else: #if the tile has been placed
                        nb-=1 #remove a dom from player's hand
                        if nb==0: #if the player has no more tiles
                            name=memProxy.getData("playerName")
                            say=say+" You have won the game! Congratulations "+name+"!" #try to be nice
                            self.onEnd(say)
                        else:
                            played.append(dom)
                            key=memProxy.getData("lastTurn") #get data
                            key[1]=False #say the player could play
                            memProxy.insertData("lasdtTurn",key) #update data
                            memProxy.insertData("tilesPlayer",nb)
                            memProxy.insertData("played",played)
                            memProxy.insertData("fringe", fringe)
                            memProxy.insertData("turn","r") #deprecated but just in case for debug
                            self.onStopped() #stop player's turn
                        self.onSay(say)
                else:
                    say="I am sorry, I didn't recognize this domino, please show it to me again"
                    self.onAgain(say)
            else:
                say="This is my domino, you cannot play it!"
                self.onAgain(say)
        else:
            say="It seems this domino has already been played!"
            self.onAgain(say)

    def onInput_onLeft(self): #hand inputs
        self.onLeft=True
    def onInput_onRight(self):
        self.onRight=True
