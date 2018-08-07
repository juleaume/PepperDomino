from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        hand=[]
        fringe=[]
        turn="null"
        played=[]
        tuto=True
        tilesPlayer=7
        pickUpTiles=14
        try:
            memProxy= ALProxy("ALMemory", "localhost",9559)
            memProxy.insertData("hand", hand)
            memProxy.insertData("fringe", fringe)
            memProxy.insertData("turn", turn)
            memProxy.insertData("played",played)
            memProxy.insertData("tuto",tuto)
            memProxy.insertData("tilesPlayer",tilesPlayer)
            memProxy.insertData("picks", pickUpTiles)
            memProxy.insertData("lastTurn", [False, False])
        except RuntimeError, e:
            self.onError
        self.onStopped()
