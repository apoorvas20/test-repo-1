
from datetime import datetime

class Spreadsheet:

    def __init__ (self):


        self.entries = [] #to store entries
        self.headers = [] #to store headers of file
    
    def loadAndParse(self, file_path):

        try:
            with open(file_path, 'r') as file:
                # lines = file.readlines()

                #read data and separate headers
                for line in file:
                    self.entries.append(line.strip())
                
                self.headers.append(self.entries[0])

                self.entries = self.entries[1:]
            
                # print(self.headers)
                # print(self.entries)
        
        except Exception as e:
            print(f"An error occured: {e}")
    
    

sheet = Spreadsheet()
sheet.loadAndParse('a.txt')
# res = sheet.filter(['color', '=', 'green'])
print(f"Final filtered answer: {res}")



