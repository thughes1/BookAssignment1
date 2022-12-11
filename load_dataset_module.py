class UserPreference:
    
    def __init__(self,filename='Users.csv'):
        ''' Produces a dictionary containing user information '''
        self.filename = filename
    
    def setFilename(self,filename):
        ''' Set filename '''
        self.filename = filename
    
    def getFilename(self):
        ''' Returns filename '''
        return self.filename
    
    def cleanDataset(self,dictionary):
        ''' Removes empty sets from the dictionary '''
        for id in dictionary.copy():
            if dictionary[id] == {}:
                del dictionary[id]
        return dictionary
    
    def loadCSV(self):
        ''' Loads csv files '''
        dictionary = {}
        try:
            with open(self.filename, encoding='ISO-8859-1') as f:
                # Skip Titles
                next(f) 
                for line in f:
                    try:
                        lineSplit = line.split(';')
                        # Remove extra quotation marks around strings
                        lineSplit = [s.strip('"') for s in lineSplit] 
                        # First value is the Key
                        id = lineSplit[0]
                        # Everything else is the Values
                        vals = lineSplit[1:]

                        if self.filename == 'Books.csv' or self.filename == 'Users.csv': 
                            dictionary[id] = tuple(vals)  
                        else:
                            # ISBN's are not unique so must check if they exist as not to overwrite them
                            ISBN = vals[0] 
                            rating = vals[1].replace('"','')
                            rating = rating.replace('\n','')
                            if id in dictionary:
                                # Append to existing key value in dict
                                dictionary[id][ISBN] = rating
                            else: 
                                # Establish new nested dictionary
                                dictionary[id] = {}
                                dictionary[id][ISBN] = rating

                    except:
                        continue
            f.close()
            return dictionary
        except :
            print('file not found!')

    def userPreference(self):
        ''' Returns a dictionary containing: ID, ISBN, Book title, author, year of publication, rating '''

        # Load csv files into dictionaries (Users.csv not required)
        user_preference = {} 
        self.setFilename('Book-Ratings.csv')
        bookRatings = self.loadCSV()
        self.setFilename('Books.csv')
        books = self.loadCSV()

        for id in bookRatings:
            user_preference[id] = {} 
            for ISBN in bookRatings[id]:
                # Not every book rated is in the Books.csv file
                if ISBN in books:
                    user_preference[id][ISBN] = {} 
                    try:
                        user_preference[id][ISBN] = list(books[ISBN])[0],list(books[ISBN])[1],list(books[ISBN])[2],bookRatings[id][ISBN]
                    except KeyError: 
                        continue
                else:
                    continue 
                    
        # Delete users that do not contain any ratings
        return self.cleanDataset(user_preference)
    
