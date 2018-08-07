from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        memProxy=ALProxy("ALMemory","localhost",9559)
        nb=memProxy.getData("tilesPlayer")
        picks=memProxy.getData("picks")
        if picks>0: #if the pile is not empty
            nb=nb+1 #add a tile to player's hand
            picks=picks-1 #remove a tile from the pile
            memProxy.insertData("tilesPlayer",nb) #update
            memProxy.insertData("picks",picks)
            say="You are picking up a tile"
        else:
            say="There are no more tiles to pick"
            key=memProxy.getData("lastTurn")
            key[1]=True #say the player could not play this turn
            memProxy.insertData("lastTurn",key)
            if key[0]:
                say="The game is over"
                self.onEnd()
        self.onStopped(say) #activate the output of the box
