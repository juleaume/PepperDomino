from naoqi import ALProxy
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        memProxy= ALProxy("ALMemory", "localhost",9559)
        hand=memProxy.getData("hand") #get the hand from memory
        if len(hand)!=0: #if the hand is not empty
            dom=hand[len(hand)-1] #the dom is the last input
            del hand[len(hand)-1] #remove last input
            memProxy.insertData("hand",hand) #update the data in memory
            if dom[0]==dom[1]: #if it is a double
                if dom[0]==0:
                    face="blank"
                else:
                    face=str(dom[0])
                say="I am removing the double"+face+"from my hand"
            else:
                if dom[0]==0:
                    lface="blank"
                else:
                    lface=str(dom[0])
                if dom[1]==0:
                    rface="blank"
                else:
                    rface=str(dom[1])
                say="I am removing %(left)s %(right)s from my hand" % {"left":lface, "right":rface}
            self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png")
        else: #if the hand is empty
            say="My hand is empty"
        self.onStopped(say)
