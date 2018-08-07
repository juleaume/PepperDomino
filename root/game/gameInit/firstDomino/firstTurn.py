from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        try:
            memProxy= ALProxy("ALMemory", "localhost",9559) #change to 9559 when working on real pepper
        except RuntimeError, e:
            self.onError()
        turn=memProxy.getData("turn") #get data from memory
        hand=memProxy.getData("hand")
        doubles=[] #the doubles of pepper's hand
        for d in hand:
            if d[0]==d[1]:
                doubles.append(d)
        if doubles!=[]: #if pepper's has double
            if max(doubles)[0]!=6: #if it is any double but 66
                if max(doubles)[0]==0:
                    maxf="blank"
                else:
                    maxf=str(max(doubles)[0])
                say="My highest double is double %s. If you have a higher double, show it to me and you may begin the game. Otherwise, show me my card before placing it on the table." % maxf
                url="qrdom/"+str(max(doubles)[0])+str(max(doubles)[1])+".png"
            else: #if it is double 6
                say="I am playing the double 6. Please show me my card before placing it on the table."
                url="qrdom/66.png"
        else: #If pepper does not have any double
            if max(hand)[0]==0:
                lmax="blank"
            else:
                lmax=str(max(hand)[0])
            if max(hand)[1]==0:
                rmax="blank"
            else:
                rmax=str(max(hand)[1])
            say="I don't have any double. If you have one, show it to me and place it on the table. If neither of us have one, please beging the highest between my %(left)s %(right)s and your highest card" % {"left" : lmax, "right" : rmax}
            url="qrdom/"+str(max(hand)[0])+str(max(hand)[1])+".png"
        self.onURL(url)
        self.onSay(say)
