from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self, p):
        canPlay=True
        try:
            memProxy= ALProxy("ALMemory", "localhost",9559) #change to 9559 when working on real pepper
        except RuntimeError, e:
            self.onError(e)
        fringe=memProxy.getData("fringe")
        turn=memProxy.getData("turn")
        hand=memProxy.getData("hand")
        table=memProxy.getData("played")
        nb=memProxy.getData("tilesPlayer")
        doubles=[]
        for d in hand: #for each domino in pepper's hand
            if d[0]==d[1]: #if the domino is a double
                doubles.append(d) #add it to the list
        dom=p[0]
        if dom[0] in range(7) and dom[1] in range(7): #if the domino is recognized
            self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png") #show it on the table
            if dom not in hand: #if the detected domino is not in the hand
                playH=False
                if dom[0]==dom[1]: #if player is playing a double
                    if dom[0]>max(doubles)[0] or doubles==[]: #if the player is playing a higher double than Pepper's
                        playH=True #they can play
                else: #if they are playing something else
                    if doubles==[]: #if Pepper has no double
                        if dom>max(hand): #if their card is higher than pepper's
                            playH=True
                if playH:
                    say="You are"
                    turn="r"
                    nb-=1
                else:
                    say="I am sorry, you cannot play that" #come on
                    self.onAgain(say) #repeat
                    canPlay=False

            else: #if the card is played from pepper's hand
                playR=False
                if doubles!=[]: #if there is some double in the list
                    if dom==max(doubles): #if the shown domino is the highest of the list
                        playR=True #allow the placement
                else: #if there is no double in the hand
                    if dom==max(hand): #if the card is pepper's highest
                        playR=True #go
                if playR: #if pepper can play
                    say="I am" #sementic
                    turn="h"
                    hand.remove(dom) #remove the domino from the hand
                else: #if the domino is not Pepper's highest
                    say="This is not the domino I am playing!" #come on
                    self.onAgain(say) #repeat
                    canPlay=False

            if dom[0]==dom[1]: #if the domino is a double
                if dom[0]==0:
                    face="blank"
                else:
                    face=str(dom[0])
                say=say+" playing the double "+face #say it
            else: #otherwise
                if dom[0]==0:
                    lface="blank"
                else:
                    lface=str(dom[0])
                if dom[1]==0:
                    rface="blank"
                else:
                    rface=str(dom[1])
                say=say + ' playing the domino %(left)s %(right)s' % {"left":lface, "right":rface} #well... don't say it is a double
            if canPlay:
                memProxy.insertData("fringe", dom) #update the data
                memProxy.insertData("played",[dom])
                memProxy.insertData("turn",turn)
                memProxy.insertData("hand",hand)
                memProxy.insertData("tilesPlayer", nb)
                self.onSay(say)
        else:
            say="I am sorry, I didn't recognize this domino, please show it to me again"
            self.onAgain(say)
            canPlay=False
