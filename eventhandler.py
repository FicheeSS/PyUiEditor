class OnClick():
    def __init__(self, clickableObj):
        self.clickableObj = clickableObj

    def checkAllClicked(self, pos):
        for cobj in self.clickableObj:
            rect = cobj.getRect()
            if rect.collidepoint(pos):
                cobj.clickcallback()


class OnHover():
    def __init__(self, hooverObject):
        self.hooverObject = hooverObject

    def checkallhover(self, pos):
        for obj in self.hooverObject:
            rect = obj.getRect()
            if rect.collidepoint(pos):
                obj.truehoovered()


class OnScroll():
    def __init__(self, scroolingobject):
        self.scroolingobject = scroolingobject

    def checkallscrool(self, pos, dir):
        for obj in self.scroolingobject:
            rect = obj.getRect()
            if rect.collidepoint(pos):
                obj.scrool(dir)


class EventHandler(OnClick, OnHover):
    def __init__(self, objectlist):
        self.objectlist = objectlist
        self.clickhandler = None
        self.hooverhandler = None
        self.updateobj()

    def updateobj(self):
        clickableObj = []
        hooverobj = []
        for obj in self.objectlist:
            if obj.getclickable():
                clickableObj.append(obj)
            if obj.gethooverable:
                hooverobj.append(obj)
            if obj.getscrollable:
                hooverobj.append(obj)
        self.clickhandler = OnClick(clickableObj)
        self.hooverhandler = OnHover(hooverobj)

    def click(self, pos):
        self.clickhandler.checkAllClicked(pos)

    def hoover(self, pos):
        self.hooverhandler.checkallhover(pos)

    def show(self):
        for obj in self.objectlist:
            obj.show()
