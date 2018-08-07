import random as rd
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        rd1=rd.randint(0,3)
        phrases=["Let's see...","Well...","What can I play?","I am thinking..."]
        say=phrases[rd1]
        self.onStopped(say) #activate the output of the box
