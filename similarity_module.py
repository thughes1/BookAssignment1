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
        self.dictionary = dictionary
    def getDictionary(self):
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
                userDict[user] = int(book[-1])
        return userDict

    def checkRated(self):
        ''' Checks whether the reader gave the book a review (1-10) '''
        d1 = self.user1
        d2 = self.user2
    
        for users in d1.copy():
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
            comparisons[user] = rank
            rank += 1
        return comparisons
        
    def commonality(self):
        ''' Removes any uncommon books from user dictionaries '''
        bookAndRatings1 = self.setUserDict(self.dictionary[self.user1]) # Converts from string of user ID to the dictionary key : value 
        bookAndRatings2 = self.setUserDict(self.dictionary[self.user2])
        
        s1 = set(bookAndRatings1)
        s2 = set(bookAndRatings2)
        sDiff = s1 ^ s2 # Symmetric difference
        
        for key in sDiff: # Removes any non-common books 
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

    def getEuclideanMetric(self): 
        ''' Returns the inverse of the sum of euclidean distance'''
        # euclidean = Sqrt of Sum of the difference in ratings squared. 
        # return 1 / (1 + (euclidean))
        # The smaller the number, the more similar
        
        self.setUp()

        if len(self.user1) == 0:
            return 0 # No similarity
        else:
            sort1 = self.sortedValues(self.user1) # Sorts book IDs in alphabetical order
            sort2 = self.sortedValues(self.user2)

            subtractPower = lambda a,b : (a - b)**2 # Applies the euclidean distance formula to the values

            euclidean = sqrt(sum(map(subtractPower,sort1,sort2)))
            similarityMetric = 1 / (1+(euclidean)) # Calculates the inverse of the similarity metric
            return similarityMetric
  
    def getCosineMetric(self):
        ''' Returns cosine similarity '''
        # Ranges from -1 (Opposite) to 1 (the same) with zero suggesting no correlation
        self.setUp()

        sort1 = self.sortedValues(self.user1)# Sorts book IDs in alphabetical order
        sort2 = self.sortedValues(self.user2)
        
        multiply = lambda a,b : a * b # Returns the numerator for our cosine calculation
        multiplications = sum(list(map(multiply,sort1,sort2)))

        square = lambda num : num ** 2 # return the denominator for our cosine calcuation
        sumSquares1 = sum(map(square,sort1))
        sumSquares2 = sum(map(square,sort2))
    
        try:
            return multiplications / (sqrt(sumSquares1)*sqrt(sumSquares2)) 
        except:
            # No correlation
            return 0 
     
    def getPearson(self):
        ''' Returns the Pearson Coefficient '''
        self.setUp()

        '''THIS PART KEEPS GETTING REPEATED THUS SHOULD MAKE NEW FUNCTION'''
        sort1 = self.sortedValues(self.user1)
        sort2 = self.sortedValues(self.user2)
        
        # Returns the mean 
        mean = lambda x : sum(x)/len(x)
        meanUser1 = mean(sort1)
        meanUser2 = mean(sort2)
        
        # Returns numerator
        subMean = lambda x,y : (x - meanUser1) * (y - meanUser2)
        numerator = sum(list(map(subMean,sort1,sort2))) 
        
        diffSqr1 = lambda x : (x - meanUser1)**2
        diffSqr2 = lambda y : (y - meanUser2)**2
        user1Diff = sum(list(map(diffSqr1,sort1)))
        user2Diff = sum(list(map(diffSqr2,sort2)))

        # Returns denominator
        denominator = sqrt(user1Diff*user2Diff) 
        try:
            return numerator/denominator
        except:
            # No similarity
            return 0 
    
    def getSpearmanCorr(self):
        ''' Returns the Spearman Correlation Coefficient '''
        self.setUp()

        if (self.user1 == 0):
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

            # Define anon function for subtracting difference squared
            sqrDiff = lambda a,b : (a-b)**2
            
            # Calculate the numerator of the equation
            numerator = 6 * sum(list(map(sqrDiff,rankedUser1,rankedUser2)))

            # Calculate the denominator of the equation
            denominator = len(rankedUser1)**3 + len(rankedUser1)
            try:
                return 1-(numerator/denominator)
            except:
                return 0 # No similarity 
        
    def getManhattan(self):
        ''' Returns the inverse of Manhattan distance '''
        self.setUp()

        if len(self.user1) == 0: # Checks if any common ratings exist
            return 0 # No similarity
        else:
            rankedUser1 = self.sortedValues(self.user1)
            rankedUser2 = self.sortedValues(self.user2)
            # Define function for calculating the difference of two ratings
            diff = lambda a,b : a-b
            manhattan = sum(list(map(diff,rankedUser1,rankedUser2)))
            return 1/(1+manhattan) # Closer to one = more similar
               
class SimilarityBooks(SimilarityUsers):
    
    def __init__(self,bookID='1'):
        ''' Initiates similarity '''
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
        
        for user in super().getDictionary():
            if self.book1 in userPref[user]:
                s1.append(user)
            if self.book2 in userPref[user]:
                s2.append(user)
        
        # Check if any users have read the books
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
            
            # Jaccard = intersect/union
            try:
                return 'Jaccard Similarity = %f' % (intersect/union) # Closer to one = more similar
            except:
                return 0 # No similarity
        
class NSimilarItems(SimilarityBooks,SimilarityUsers):
    
    def __init__(self,bookID=None,userID=None):
        super().__init__()
        #super(SimilarityUsers,self).__init__()
        #super(SimilarityBooks,self).__init__()
        # Both are initialised as null to allow for Boolean operation later
        self.__bookID = bookID
        self.__userID = userID
    
    def setUserID(self,user):
        self.__userID = user
        
    def setBookID(self,book):
        self.__bookID = book
    
    def getUserID(self):
        return self.__userID
    def getBookID(self):
        return self.__bookID
    
    def getUnion(self,users):
        ''' Gets users who form a union with the bookID '''
        usersWUnion = []

        for user in users:
            if self.__bookID in users[user]:
                usersWUnion.append(user)
            else:
                continue

        return usersWUnion
    
    def bookCompare(self,users):
        ''' Extracts books to compare from our list of common raters '''
        books = []

        for user in users: # Cycle through users
            for isbn in super().getDictionary()[user].keys():
                if isbn in books:
                    next
                else:
                    books.append(isbn)
        books.remove(self.__bookID) # Delete comparison book we are comparing against
        return books
    
    def reduceDataset(self):
        ''' Reduces dataset to users that contain comparable data '''
        # Remove any zeroes as they are not comparable
        # Similar to super().checkRated() however this only modifies one user not two
        dictionary = super().getDictionary()

        d1 = dictionary[self.__userID]
        for books in d1.copy():
            if '0' in d1[books]:
                del d1[books]
            else:
                continue

        for user in dictionary.copy():
            b = 0 # Initialise b for books 
            for book in d1:
                if book in dictionary[user]:
                    b+=1 # Do not delete if at least one book exists 
                else:
                    continue
            if b == 0: # If no common books we delete
                del dictionary[user]
        return dictionary
                        
    def setUserDict(self,users):
        ''' Convert dictionary item to the correct format {'ISBN':Rating} '''
        userDict = {}
        for user in list(users):
            for book in list(users.values()):
                userDict[user] = int(book[-1])
        return userDict
    
    def getNSimilarItems(self,similarityMetric,numberOfElements):
        ''' Returns n similar items to item '''
        rankings = {}#  Defines users dictionary with opposing similarity rating
        userPreference = super().getDictionary()
        
        if self.__userID != None:
            userPreference = self.reduceDataset()
            length = len(userPreference)
            i = 0
            for user in userPreference:
                print('%d%%' % ((i/length)*100),end='\r')
                super().setUser1(self.__userID) # This must be reset each time due to it being removed in commonality...
                super().setUser2(user)
                if super().getUser2 == super().getUser1(): # Don't compare to itself
                    next
                else:
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
                rankings[user] = similarity
        
        elif self.__bookID != None:
            # Similarity = Intersect / Union --> Therefor no similar users would result in a value of zero --> therefore we only need to test where Union exists!!!
            #return self.bookCompare(self.getUnion(userPreference),userPreference)
            super().setBook1(self.__bookID)
            booksToCompare = self.bookCompare(self.getUnion(userPreference))
            length = len(booksToCompare)
            i=0
            for book in booksToCompare:
                print('%d%%' % ((i/length)*100),end='\r')
                i+=1 
                super().setBook2(book)
                rankings[book] = super().getSimilarity()
      
        else:
            print('Book or user not specified')
        
        # Reset in case called again without being instantiated as a new object
        self.__bookID = None         
        self.__userID = None 
        return sorted(rankings.items(), key = lambda x:x[1], reverse = True)[:numberOfElements] # Returns list, sorted largest -> smallest
    
'''
up = UserPreference()
dictionary = up.userPreference()
sim = SimilarityUsers()
'''
def setUserDict(users):
    userDict = {}
    for user in list(users):
        for book in list(users.values()):
            userDict[user] = int(book[-1])
    return userDict

def testUser():
    sim = SimilarityUsers()
    user1 = '276772'
    user2 = '11676'
    sim.setUser1(user1)
    sim.setUser2(user2)
    print(sim.getEuclideanMetric())
#testUser()
    
def testUserSim(dictionary,sim):

    start_time = time.time()

    user1 = dictionary['276772']
    user1Dict = {}
    user2 = dictionary['11676'] 
    user2Dict = {}

    #print(list(user1.values())[0][-1])
    user1Dict = setUserDict(user1)
    user2Dict = setUserDict(user2)


    sim.setUser1(user1Dict)
    sim.setUser2(user2Dict)
    print(sim.getCosineMetric())

    print(time.time() - start_time) # TAKES circa 35 SECONDS!
    
#testUserSim(dictionary,sim)

def testBooks():
    start_time = time.time()
    sim = SimilarityBooks()
    sim.setBook1('0345339711')
    sim.setBook2('059035342X')
    print(sim.getSimilarity())
    print(time.time() - start_time)
#testBooks()

def testNSim():
    start_time = time.time()
    sim = NSimilarItems()
    #sim.setUserID('11676')
    #print(sim.getNSimilarItems('Euclidean',dictionary))
    sim.setBookID('0345339711')
    #sim.getNSimilarItems('Euclidean',dictionary) # Shouldn't need to specify a sim metric here
    #sim.setUserID('276925')
    #dictionary = sim.reduceDataset(dictionary) # Greatly reduces the dataset to iterate over
    print((sim.getNSimilarItems('Euclidean',50)))
    print(time.time()-start_time)
#testNSim()            



