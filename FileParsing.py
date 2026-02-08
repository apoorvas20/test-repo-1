
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
    
    def filter(self, criteria: list):

        '''
        criteria = ['color', '=', 'green']

        For multiple entries for a gievn filer, assuming to return the latest record. 
        i.e. max(date)
        to compare the dates--> convert them to datetime object

        '''

        #if any arr > len 3
        if len(criteria) > 3:
            raise ValueError('Craiteria Arr should be length 3')

        # colName = criteria[0]
        # operator = criteria[1]
        filter = criteria[2]

        #define date format
        date_format = '%Y/%m/%d'

        filtered_rows = []
        maxDate = None

        for entry in self.entries:
            # print(entry)
            curr = entry.split()
            # print(curr, "current data")
            # print(curr[2], "date")
            if filter == curr[0]:
                filtered_rows.append(entry)
                currDate = datetime.strptime(curr[1], date_format)
                if not maxDate or currDate > maxDate:
                    maxDate = currDate
                    res = entry
        
        return res

sheet = Spreadsheet()
sheet.loadAndParse('a.txt')
res = sheet.filter(['color', '=', 'green'])
print(f"Final filtered answer: {res}")



