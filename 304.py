class StringHandler:
    
    def getString(self):
        self.text = input()
    
    def printString(self):
        print(self.text.upper())


obj = StringHandler()
obj.getString()
obj.printString()
