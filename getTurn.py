from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        memProxy = ALProxy("ALMemory","localhost",9559) #change to 9559

        #get data. Val can be int, float, list, string
        val = memProxy.getData("turn")
        if val=="h":
            self.onStoppedH() #activate the output of the box
        elif val=="r":
            self.onStoppedR()
        else:
            self.onStopped(str(val))
