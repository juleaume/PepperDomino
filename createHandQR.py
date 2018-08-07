from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self, p):
        try:
            memProxy= ALProxy("ALMemory", "localhost",9559) #change to 9559 when working on real pepper
        except RuntimeError, e:
            self.onError()
        hand=memProxy.getData("hand") #get the hand from the memory
        red=[0xff,0x00,0x00] #colours, but a bit deprecated
        green=[0x00, 0xff, 0x00]
        blue=[0x00, 0x00, 0xff]
        yellow=[0xff, 0xff, 0x00]
        magenta=[0xff, 0x00, 0xff]
        cyan=[0x00, 0xff, 0xff]
        if len(hand)<7: #if the hand is not complete
            flagDouble=True #assume the domino is new
            dom=[p[0][0],p[0][1]] #set dom from data
            for d in hand: #for each domino in the current hand
                if d==dom: #if the domino is already found
                    say="It seems I already have this domino!"
                    flagDouble=False #do not add it to the hand
                    self.showLed(red)
                    self.onAgain()
            if flagDouble: #if you can add it to the hand
                if dom[0] in range(7) and dom[1] in range(7): #if the domino exists
                    self.onURL("qrdom/"+str(dom[0])+str(dom[1])+".png") #show it on the tablet
                    if dom==[6,6]: #if the domino is 66
                        say='I add the double 6 to my hand, and I will start the game. '
                        self.showLed(yellow)
                        memProxy.insertData("turn", "r") #assume the robot will start the game
                    else:
                        if dom[0]==dom[1]: #if it is any double
                            if dom[0]==0:
                                side="blank"
                            else:
                                side=str(dom[0])
                            say="I add the double " + side + " to my hand. " #speaks
                            self.showLed(cyan)
                        else: #if it is any other domino
                            say='I add the domino %(left)d %(right)d to my hand. ' % {"left":dom[0], "right":dom[1]} #speaks
                            self.showLed(green) #detected
                    hand.append(dom) #add the domino to the hand
                    memProxy.insertData("hand", hand) #add the hand to the memory
                    if len(hand)==7: #if the hand is full
                        say=say+" Are my tiles correct? If yes, let's start the game by touching my hand!"
                        self.onHand()
                    self.onAgain() #no else because the hand might not be correct
                else:
                    say="I am sorry, I didn't recognize this domino"
                    self.showLed(red)

        else:
            say="I already have all my dominoes, let's start the game by touching my hand!"
            self.showLed(red)
            self.onHand()
        self.onSay(say)

    def showLed(self, p):
        ids = []
        leds = ALProxy("ALLeds")
        sGroup = "FaceLeds"
        id = leds.post.fadeRGB(sGroup, 256*256*p[0] + 256*p[1] + p[2], 0.1)
        ids.append(id)
        leds.wait(id, 0)
        ids.remove(id)
