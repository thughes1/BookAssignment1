#!/usr/bin/env python
# coding: utf-8

# In[34]:


class UserPreference:
    
    def __init__(self,filename='Users.csv'):
        ''' Init object '''
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
        ''' Loads the relevant csv files'''
        dictionary = {} # Init dictionary 
        try:
            with open(self.filename, encoding='ISO-8859-1') as f:
                next(f) # Skip the titles
                for line in f:
                    try:
                        lineSplit = line.split(';') # Use semi-colon as deliminater
                        lineSplit = [s.strip('"') for s in lineSplit] # Remove extra quotation marks
                        id = lineSplit[0] # First value is unique identifier
                        vals = lineSplit[1:] # Everything else 
                        if self.filename == 'Books.csv' or self.filename == 'Users.csv': # != not working for some reason
                            dictionary[id] = tuple(vals)  
                        else:
                            ISBN = vals[0] # Unique identifier for book
                            rating = vals[1].replace('\n','') # Rating given to book
                            if id in dictionary:
                                # Append to existing key value in dict
                                dictionary[id][ISBN] = rating
                            else: 
                                # Establish new nested dictionary
                                dictionary[id] = {}
                                dictionary[id][ISBN] = rating

                    except: # In case values cannot be split 
                        continue
            f.close()
            return dictionary # Returns csv file as dictionary in form, id:{var1,var2,...,varn}
        except :
            print('file not found!')

    def userPreference(self):
        ''' Returns a dictionary containing: ID, ISBN, Book title, author, year of publication, rating '''

        user_preference = {} # IDs, ISBN, Book title, author, year of publication, rating
        self.setFilename('Book-Ratings.csv')
        bookRatings = self.loadCSV()
        self.setFilename('Books.csv')
        books = self.loadCSV()

        for id in bookRatings:
            
            user_preference[id] = {} # Init user_preference sub dictionary for IDs
            for ISBN in bookRatings[id]:
                if ISBN in books:
                    user_preference[id][ISBN] = {} # Init user_preference sub dictionary for ISBN
                    try:
                        user_preference[id][ISBN] = list(books[ISBN])[0],list(books[ISBN])[1],list(books[ISBN])[2],bookRatings[id][ISBN]
                    except KeyError: # Exception in case ISBN doesn't exist
                        continue
                else:
                    continue # If book reviewed is not in books then skip to next book
                    
        # Delete empty sets 
        return self.cleanDataset(user_preference)
    


'''userPreferences = UserPreference()
userPreferences.userPreference()
'''

# In[ ]:





# In[ ]:




