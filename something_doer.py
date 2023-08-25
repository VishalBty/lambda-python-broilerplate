from config import *

class SomethingDoer:
    def __init__(self, database):
        self.database = database
    
    def do_it(self):
        print(self.database)