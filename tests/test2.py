class Point:
    def __init__(self, s):
        self.path = s

    def __eq__(self, otherStr):
        return self.path == otherStr

class Test():
    def __init__(self):
        pass
    # Dictionaries are more efficient than list of tuples
    # since they jump straight to the key instead
    # of searching each element in the array like
    # arrays do

    def doGet(self):
        ACTIONS = {
            '/links': printQuit
        }
        for condition in ACTIONS:
            if self.path == condition:
                ACTIONS[condition]()
                return
            action_default()
            
    
def printQuit():
    # some action or function here
    print("Nothing")
    pass

def action_default():
    print("Default function")
    pass

def act2():
    print('help')

Test.doGet(Point('/links'))
Test.doGet(Point('/'))