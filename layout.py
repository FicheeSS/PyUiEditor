from locals import *

class Layout():
    def __init__(self, stickypos, window, size=[50,50]):
        t = 0 
        for i in range(LAYOUTRANGE[0],LAYOUTRANGE[1]) :
            if stickypos != i : 
                t += 1
        if t == LAYOUTRANGE[1]:
            raise ReferenceError
        self.stickypos = stickypos
        self.objlist = []
        self.window = window
        self.size = size
        
    def addobj(self, obj):
        if type(obj) == list :
            for o in obj :
                self.objlist.append(o)
        else : 
            self.objlist.append(obj)
    
    def calculuatepos(self):
        for obj in objlist :
           rect = obj.getRect() 
           size = obj.getsize()
    
    def show(self):
        for obj in self.objlist :
            obj.show()
        