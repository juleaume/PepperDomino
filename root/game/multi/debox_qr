class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        self.bFirstTime = True

    def onUnload(self):
        self.bFirstTime = True

    def onInput_reset(self):
        self.bFirstTime = True

    def onInput_onStart(self, p):
        if len(p)!=0:
            datas=[]
            centroids=[]
            for i in range(len(p)):
                rdata=p[i][0] #raw data
                l=int(rdata[1]) #data extraction
                r=int(rdata[3])
                data=[l,r]  #data format [[l,r],[xc,yc]]
                datas.append(data)
            if( self.bFirstTime ):
                self.bFirstTime = False
                self.data(datas)
