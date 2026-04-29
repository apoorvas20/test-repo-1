
from datetime import datetime

class Spreadsheet:

    def __init__ (self):


        self.entries = [] #to store entries
        self.headers = [] #to store headers of file
    
    
    
    

sheet = Spreadsheet()
sheet.loadAndParse('a.txt')
res = sheet.filter(['color', '=', 'green'])
print(f"Final filtered answer: {res}")



