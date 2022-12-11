from load_dataset_module import UserPreference
from math import sqrt
import time

class SimilarityUsers:
    
    def __init__(self,similarityMetric='euclidean',user={'BookID':1},dictionary = UserPreference().userPreference()):
        ''' Initialise the object '''
        self.similarityMetric = similarityMetric
        self.user1 = user
        self.user2 = user
        self.dictionary = dictionary
    
    def setDictionary(self,dictionary):
        ''' Defines dictionary '''
        self.dictionary = dictionary
    def getDictionary(self):
        ''' Returns userPreference (Unless set otherwise)'''
        return self.dictionary
        
    def setUser1(self,user):
        ''' Sets dictionary containing books(ISNB) and corresponding rating for user1 '''
        self.user1 = user
    def getUser1(self):
        ''' Returns dictionary containing books(ISBN) and correspondin rating for user1 '''
        return self.user1
    
    def setUser2(self,user):
        ''' Sets dictionary containing books(ISNB) and corresponding rating for user2 '''
        self.user2 = user  
    def getUser2(self):
        ''' Returns dictionary containing books(ISBN) and correspondin rating for user2 '''
        return self.user2 
    
    def setSimilarityMetric(self,similarityMetric):
        ''' Sets similarity metric '''
        self.similarityMetric = similarityMetric
    def getSimilarityMetric(self):
        ''' Returns similarity metric '''
        return self.similarityMetric

    def setUserDict(self,users):
        ''' Sets value to correct format '''
        userDict = {}
        for user in list(users):
            for book in list(users.values()):
                # Sets the value as the rating 
                userDict[user] = int(book[-1])
        return userDict

    def checkRated(self):
        ''' Checks whether the reader gave the book a review (1-10) '''
        d1 = self.user1
        d2 = self.user2
    
        for users in d1.copy():
            # If rating was zero (Implicit) remove from the comparison set
            if d1[users] == 0 or d2[users] == 0:
                del d1[users]
                del d2[users]
            else:
                continue

        self.setUser1(d1)
        self.setUser2(d2)
        
    def rankUsers(self,comparisons):
        ''' Returns a dictionary with values replaced by their rank '''
        rank = 1
        for user in comparisons:
            # Overwriite value with rank
            comparisons[user] = rank
            rank += 1
        return comparisons
        
    def commonality(self):
        ''' Removes any uncommon books from user dictionaries '''
        bookAndRatings1 = self.setUserDict(self.dictionary[self.user1]) 
        bookAndRatings2 = self.setUserDict(self.dictionary[self.user2])
        
        # Calculate symmetric difference
        s1 = set(bookAndRatings1)
        s2 = set(bookAndRatings2)
        sDiff = s1 ^ s2 
        
        # Removes any non-common books 
        for key in sDiff: 
            if key in bookAndRatings1:
                del bookAndRatings1[key]
            if key in bookAndRatings2:
                del bookAndRatings2[key]

        self.user1 = bookAndRatings1
        self.user2 = bookAndRatings2
        
    def sortedValues(self,user):
        ''' Items are sorted by key then put into a list containing their values in the same order '''
        return dict(sorted(user.items())).values()

    def setUp(self):
        ''' Sets up data such that similarity metric may be carried out '''
        self.commonality()
        self.checkRated()
        sort1 = self.sortedValues(self.user1)
        sort2 = self.sortedValues(self.user2)

    def getEuclideanMetric(self): 
        ''' Returns the inverse of the sum of euclidean distance'''
        
        self.setUp()

        if len(self.user1) == 0:
             # No similarity
            return 0
        else:
            # Applies the euclidean distance formula to the values
            subtractPower = lambda a,b : (a - b)**2 
            euclidean = sqrt(sum(map(subtractPower,self.user1,self.user2)))
            # Calculates the inverse of the similarity metric
            similarityMetric = 1 / (1+(euclidean)) 
            # Closer to one is more similar
            return similarityMetric
  
    def getCosineMetric(self):
        ''' Returns cosine similarity '''
        self.setUp()

        if len(self.user1) == 0:
            # No similarity
            return 0
        else:
            # Returns the numerator for our cosine calculation
            multiply = lambda a,b : a * b 
            multiplications = sum(list(map(multiply,self.user1,self.user2)))

            # return the denominator for our cosine calcuation
            square = lambda num : num ** 2 
            sumSquares1 = sum(map(square,self.user1))
            sumSquares2 = sum(map(square,self.user2))
        
            try:
                # Ranges from -1 (Opposite) to 1 (the same) with zero suggesting no correlation
                return multiplications / (sqrt(sumSquares1)*sqrt(sumSquares2)) 
            except:
                # No correlation
                return 0 
        
    def getPearson(self):
        ''' Returns the Pearson Coefficient '''
        self.setUp()

        if len(self.user1) == 0:
            # No similarity
            return 0
        else:
            
            # Returns the mean 
            mean = lambda x : sum(x)/len(x)
            meanUser1 = mean(self.user1)
            meanUser2 = mean(self.user2)
            
            # Returns numerator
            subMean = lambda x,y : (x - meanUser1) * (y - meanUser2)
            numerator = sum(list(map(subMean,self.user1,self.user2))) 
            
            # Returns denominator
            diffSqr1 = lambda x : (x - meanUser1)**2
            diffSqr2 = lambda y : (y - meanUser2)**2
            user1Diff = sum(list(map(diffSqr1,self.user1)))
            user2Diff = sum(list(map(diffSqr2,self.user2)))
            denominator = sqrt(user1Diff*user2Diff) 

            try:
                # High Correlation: |0.50 - 1.00|
                # Medium Correlation: |0.30 - 0.49|
                # Low Correlation: |> 0.29| 
                return numerator/denominator
            except:
                # No similarity
                return 0 
        
    def getSpearmanCorr(self):
        ''' Returns the Spearman Correlation Coefficient '''
        self.setUp()

        if len(self.user1 == 0):
            return 0
        else:
            # Sorts dict by value in descending order
            rankedUser1 = dict(sorted(self.user1.items(), key = lambda x:x[1], reverse = True)) 
            rankedUser2 = dict(sorted(self.user2.items(), key = lambda x:x[1], reverse = True))

            # Replace the value with the ranking'
            rankedUser1 = self.rankUsers(rankedUser1)
            rankedUser2 = self.rankUsers(rankedUser2)

            # Order values by their key as opposed to rank
            rankedUser1 = self.sortedValues(rankedUser1)
            rankedUser2 = self.sortedValues(rankedUser2)

            # returns difference squared
            sqrDiff = lambda a,b : (a-b)**2
            
            # Calculate the numerator of the equation
            numerator = 6 * sum(list(map(sqrDiff,rankedUser1,rankedUser2)))

            # Calculate the denominator of the equation
            denominator = len(rankedUser1)**3 + len(rankedUser1)
            try:
                # Value of one denotes perfect similarity
                return 1-(numerator/denominator)
            except:
                return 0 # No similarity 
        
    def getManhattan(self):
        ''' Returns the inverse of Manhattan distance '''
        self.setUp()

        if len(self.user1) == 0: 
            return 0 # No similarity
        else:

            # Define function for calculating the difference of two ratings
            diff = lambda a,b : a-b
            manhattan = sum(list(map(diff,self.user1,self.user2)))
            try:
                # Value of one denotes perfect similarity
                return 1/(1+manhattan) 
            except:
                # No similarity
                return 0
                
class SimilarityBooks(SimilarityUsers):
    
    def __init__(self,bookID='1'):
        ''' Compares two books '''
        super().__init__()
        self.book1 = bookID
        self.book2 = bookID
            
    def setBook1(self,bookID):
        ''' Sets book1 '''
        self.book1 = bookID
    def setBook2(self,bookID):
        ''' Sets book2 '''
        self.book2 = bookID
    
    def getBook1(self):
        ''' Returns book1 dictionary '''
        return self.book1 
    def getBook2(self):
        ''' Returns book2 dictionary '''
        return self.book2
     
    def getSimilarity(self):
        ''' Returns Jaccard similarity metric '''
        s1 = []
        s2 = []
        userPref = super().getDictionary()

        # Check if any users have read the books
        for user in super().getDictionary():
            if self.book1 in userPref[user]:
                s1.append(user)
            if self.book2 in userPref[user]:
                s2.append(user)
        if s1 == [] and s2 == []:
            return 'Could not find either book in dataset'
        elif s2 == []:
            return 'Could not find book 2 in dataset'
        elif s1 == []:
            return 'Could not find book 1 in dataset'
        else:
            
            # Converts lists to sets for intersection and union functions
            s1 = set(s1)
            s2 = set(s2)
            
            # Calculate the intersect and union
            intersect = len(s1.intersection(s2))
            union = len(s1.union(s2))
            
            try:
                # Value of one denotes perfect similarity
                return 'Jaccard Similarity = %f' % (intersect/union) 
            except:
                return 0 # No similarity
        
class NSimilarItems(SimilarityBooks,SimilarityUsers):
    
    def __init__(self,bookID=None,userID=None):
        ''' Calculates N similar items '''
        super().__init__()
        # Both are initialised as None to allow for Boolean operation later
        self.__bookID = bookID
        self.__userID = userID
    
    def setUserID(self,user):
        ''' Sets user ID '''
        self.__userID = user
    def setBookID(self,book):
        ''' Sets book ID '''
        self.__bookID = book
    
    def getUserID(self):
        ''' Returns user ID '''
        return self.__userID
    def getBookID(self):
        ''' Return book ID'''
        return self.__bookID
    
    def getUnion(self,users):
        ''' returns users who have read the book '''
        usersWUnion = []
        # If user has read the book, add them to the list to compare
        for user in users:
            if self.__bookID in users[user]:
                usersWUnion.append(user)
            else:
                continue

        return usersWUnion
    
    def bookCompare(self,users):
        ''' Extracts books to compare from our list of common raters '''
        books = []
        # Produce a list of unique books to compare
        for user in users: 
            for isbn in super().getDictionary()[user].keys():
                if isbn in books:
                    next
                else:
                    books.append(isbn)
        # Delete the book we are producing similarities against
        books.remove(self.__bookID) 
        return books
    
    def reduceDataset(self):
        ''' Reduces dataset to users that contain comparable data '''
        
        userPref = super().getDictionary()

        # Removes any books that userID has read that are not given an explicit rating (<10)
        books = userPref[self.__userID]
        for book in books.copy():
            if '0' in books[book]:
                del books[book]
            else:
                continue
        # For each user, check whether they have any books that are comparable
        # If not delete to reduce the dataset
        for user in userPref.copy():
            b = 0 
            for book in books:
                if book in userPref[user]:
                    b+=1 
                else:
                    continue
            # No common books, thus delete
            if b == 0: 
                del userPref[user]
        return userPref
                        
    def setUserDict(self,users):
        ''' Convert dictionary item to the correct format {'ISBN':Rating} '''
        userDict = {}
        for user in list(users):
            for book in list(users.values()):
                userDict[user] = int(book[-1])
        return userDict
    
    def getNSimilarItems(self,similarityMetric,numberOfElements):
        ''' Returns n similar items to item '''
        rankings = {}
        userPreference = super().getDictionary()
        
        if self.__userID != None:
            userPreference = self.reduceDataset()
            length = len(userPreference)
            i = 0
            for user in userPreference:
                # Shows percentage of completion
                print('%d%%' % ((i/length)*100),end='\r')
                # This must be reset each time due to it being removed in super().commonality()
                super().setUser1(self.__userID) 
                super().setUser2(user)
                # Don't compare to itself
                if super().getUser2 == super().getUser1(): 
                    next
                else:
                    # Applies similarity metric
                    if similarityMetric == 'Euclidean':
                        similarity = super().getEuclideanMetric()
                    elif similarityMetric == 'Cosine':
                        similarity = super().getCosineMetric()
                    elif similarityMetric == 'Spearman':
                        similarity = super().getSpearmanCorr()
                    elif similarityMetric == 'Pearson':
                        similarity = super().getPearson()
                    else:
                        similarity = super().getManhattan() 
                # Assigns associated similarity to user
                rankings[user] = similarity
        
        elif self.__bookID != None:
            # Similarity = Intersect / Union --> 
            # Therefore no similar users would result in a value of zero --> 
            # therefore we only need to test where Union exists
            
            super().setBook1(self.__bookID)
            # Reduces dataset to Comparable books only
            booksToCompare = self.bookCompare(self.getUnion(userPreference))
            length = len(booksToCompare)

            i=0
            for book in booksToCompare:
                # Show percentage of completion
                print('%d%%' % ((i/length)*100),end='\r')
                i+=1 
                super().setBook2(book)
                # Assign associated ranking to book
                rankings[book] = super().getSimilarity()
      
        else:
            print('Book or User not specified')
        
        # Reset in case called again without being instantiated as a new object
        self.__bookID = None         
        self.__userID = None 
        # Returns N similar items in order of their ranking 
        return sorted(rankings.items(), key = lambda x:x[1], reverse = True)[:numberOfElements] 
