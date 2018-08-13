from naoqi import ALProxy
import numpy as np

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        memProxy=ALProxy("ALMemory", "localhost",9559)
        hand=memProxy.getData("hand") #get the data from the memory
        fringe=memProxy.getData("fringe")
        played=memProxy.getData("played")
        ambigu=False #set the flag to flase

        if len(fringe)!=0 and len(hand)!=0:
            token=selectToken(hand,fringe)
            if not token==[]:
                dom=token[0]
                side=token[1]
                if not (fringe[0]==dom[side] or fringe[1]==dom[side]):
                    side=(token[1]+1)%2

        if token!=[]: #if the input is not empty
            if dom in hand: #if the domino is in the hand (just to be sure)
                played.append(dom) #add the domino to the array of the played
                hand.remove(dom) #remove it from the hand
                memProxy.insertData("hand",hand) #update the memory
                if dom[0]==dom[1]:
                    if dom[0]==0:
                        face="blank"
                    else:
                        face=str(dom[0])
                    say="I am playing the double "+face
                else:
                    if dom[0]==0:
                        lface="blank"
                    else:
                        lface=str(dom[0])
                    if dom[1]==0:
                        rface="blank"
                    else:
                        rface=str(dom[1])
                    say="I am playing the domino %(left)s %(right)s" %{"left": lface, "right": rface} # + "with the side "+ str(dom[side]) #sementic
                self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png") #show tablet
                #if the domino can be placed on both side of the fringe AND the domino is not a double
                if (dom==fringe or dom==[fringe[1],fringe[0]]) and not dom[0]==dom[1]:
                    say+=" next to the side "+str(dom[side]) #tell next to what you place it
                if not fringe[0]==fringe[1]:
                    for i in range(2):
                        if dom[side]==fringe[i]:
                            fringe[i]=dom[(side+1)%2]
                else:
                    fringe[0]=dom[(side+1)%2] #arbitrary

                memProxy.insertData("fringe",fringe) #update the memory
                memProxy.insertData("turn","h")
                memProxy.insertData("played",played)
                if len(hand)==0: #if pepper's hand is empty
                    say=say+". I have won the game! "
                    self.onEnd(say) #finish the game
                else: #if it is not empty
                    key=memProxy.getData("lastTurn")
                    key[0]=False #say it played
                    memProxy.insertData("lasdtTurn",key)
                    self.onPlayer() #player's turn
            else:
                say="I might have a problem with my tiles..."
        else: #if the tile is empty
            nb=memProxy.getData("picks") #get data
            if nb>0: #if there is still tiles to pick
                nb-=1 #remove one
                memProxy.insertData("picks", nb) #update the memory
                say="I need to pick up a tile. Please show me the tile I am picking"
                self.onPick() #pick a tile
            else: #if there is no more tiles to pick
                say="I cannot play this turn"
                key=memProxy.getData("lastTurn")
                key[0]=True #watchdog for last turn
                memProxy.insertData("lasdtTurn",key) #update
                if key[1]: #if player couldn't play last turn either
                    scoref=0
                    for d in hand:
                        scoref+=d[0]+d[1]
                    say="The game is over! I have " + str(scoref)+ " points " #end the game
                    d=[]
                    for i in range(7):
                        for j in range(i,7):
                            d.append([i,j])
                    m=np.ones(len(d))
                    for dom in hand:
                        if dom in d:
                            m[d.index(dom)]=0
                    for dom in played:
                        if dom in d:
                            m[d.index(dom)]=0
                    sp=0
                    for i in range(28):
                        if m[i]==1:
                            sp+=d[i][0]+d[i][1]
                    say+="and you should have " + str(sp) + " points that means "
                    if sp>scoref:
                        say+="I have won the game!"
                    elif sp<scoref:
                        say+="You have won the game! Congratulations!"
                    else:
                        "This is a draw!"
                    self.onEnd(say)
                else:
                    self.onPlayer()
        self.onSay(say) #activate the output of the box

def selectToken(h, f): #v3.1
    index=-1 #index to be returned
    indexa=[] #list of potential returns
    scorea=[]
    side=[]
    hs=0 #highest score
    ihs=-1 #index of the highest score
    noReturn=False
    for i in range(2): #for each side of the fringe
        for j in range(len(h)): #for each domino in the hand
            for k in range(2): #for each side of the domino
                if h[j][k]==f[i]: #if there is a match
                    indexa.append(j)
                    scorea.append(h[j][0]+h[j][1])
                    side.append(k)
                    for di in range(len(h)):
                        if not di==j and (h[j][(k+1)%2]==h[di][0] or h[j][(k+1)%2]==h[di][1]):
                            score=h[j][0]+h[j][1]+h[di][0]+h[di][1]
                            if score>hs:
                                hs=score
                                index=j
    if index==-1:
        if len(indexa)>0:
            ihs=max(enumerate(scorea))[0]
            index=indexa[ihs]
        else:
            noReturn=True
            return []
    if not noReturn:
        if ihs==-1:
            ihs=max(enumerate(scorea))[0]
        return [h[index],side[ihs]]
