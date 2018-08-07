from naoqi import ALProxy as al
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self, p):
        mem=ALProxy("ALMemory","localhost",9559)
        mem.insertData("playerName",p)
