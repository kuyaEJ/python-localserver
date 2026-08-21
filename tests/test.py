class Point:
    def __init__(self, s):
        self.path = s

    def __eq__(self, otherStr):
        return self.path == otherStr

class Test():
    def __init__(self):
        pass
        
    def doGet(self):
        ACTIONS = [
            (lambda u: u.path == '/links', printQuit)
        ]
        for condition, action in ACTIONS:
            if condition(self):
                action()
                return
            action_default()

def printQuit():
    # some action or function here
    print("Nothing")
    pass

def action_default():
    print("Default function")
    pass


Test.doGet(Point('/links'))
Test.doGet(Point('/'))