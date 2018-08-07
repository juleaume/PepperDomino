from naoqi import ALProxy as alp
import random as rd

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        mP=ALProxy("ALMemory","localhost",9559)
        hand=mP.getData("hand")
        fringe=mP.getData("fringe")
        block=False
        fl=fringe[0]
        fr=fringe[1]
        l=self.dom[0]
        r=self.dom[1]
        phrases=["well done","I wasn't expecting that","Good job","Oh, impressive"]
        for d in hand:
            if d[0]==l or d[0]==r or d[1]==l or d[1]==r and not fl==fr:
                phrases=["Oh no, I wanted to play my tile here, well done!", "Ah, I could have played here", "You took my spot, good job", "you blocked me, well done"]
                break
        r=rd.randint(0,len(phrases)-1)
        say=phrases[r]
        self.onStopped(say) #activate the output of the box

    def onInput_onPlayed(self, p):
        self.dom=p[0]
