from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self, p):

        try:
            memProxy= ALProxy("ALMemory", "localhost",9559) #change to 9559 when working on real pepper
        except RuntimeError, e:
            self.onError(e)
        hand=memProxy.getData("hand")
        played=memProxy.getData("played")
        fringe=memProxy.getData("fringe")
        dom=p[0]
        if dom not in played and dom not in hand:
            if dom[0] in range(7) and dom[1] in range(7):
                self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png")
                hand.append(dom)
                memProxy.insertData("hand", hand)
                say="I am picking %(left)d %(right)d." % {"left":dom[0], "right":dom[1]}
                blocked=True
                for d in hand:
                    for f in fringe:
                        if d[0]==f or d[1]==f:
                            blocked=False
                if not blocked:
                    say=say+" Great, I might play next turn!"
                self.onStopped()

            else:
                say="I am sorry, I didn't recognize this domino, please show it to me again"
                self.onAgain(say)
        else:
            say="It seems this tiles has already been played"
            self.onAgain(say)
        self.onSay(say)
