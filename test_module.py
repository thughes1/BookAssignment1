import load_dataset_module
from similarity_module import SimilarityUsers as sUsers
from similarity_module import SimilarityBooks as sBooks
from similarity_module import NSimilarItems as nItems

def getSimilarity(comparisonType):
    ''' Returns similarity between two users '''
    print('Please select the distance metric desired')
    try:
        similarityMetric = int(input('Euclidean: 0, Manhattan: 1, Pearson: 2, Spearman: 3, Cosine: 4 '))
        # Ensures value entered is valid, i.e. 0-4
        if abs(similarityMetric) < 5:
            if comparisonType == 0:
                return compare2Users(similarityMetric)
            else:
                return compareNUsers(similarityMetric)
        else:
            print('Please ensure value entered is between 0 and 4')
            return getSimilarity()
    except ValueError:
        print('Please ensure value entered is an integer')
        return getSimilarity(comparisonType)

def compare2Books():
    ''' Returns similiarity score between two books '''
    book1 = input('Please enter the ISBN of the first book: ')
    book2 = input('Please enter the ISBN of the second book: ')
    sim = sBooks() 
    sim.setBook1(book1)
    sim.setBook2(book2)
    #0345339711
    #059035342X
    return sim.getSimilarity()

def compareNBooks():
    ''' Returns list of similarities '''
    bookID = input('Please enter the ISBN of the book you want to compare: ')
    sim = nItems()
    sim.setBookID(bookID)
    #0345339711
    try:
        numElements = int(input('Please enter how many elements you would like to compare to: '))
    except ValueError:
        print('Please ensure value entered is an integer')
        return compareNBooks()
    print('Comparison may take some time...')
    return sim.getNSimilarItems(None,numElements) 

def compare2Users(similarityMetric):
    ''' Calculates similarity between two users '''
    user1 = input('Please enter the ID of the first user: ')  
    user2 = input('Please enter the ID of the second user: ') 
    sim = sUsers()
    sim.setUser1(user1)
    sim.setUser2(user2)
    #276772
    #11676
    if similarityMetric == 0: # Euclidean Distance
        return sim.getEuclideanMetric()
    elif similarityMetric == 1: # Manhattan Distance
        return sim.getManhattan()
    elif similarityMetric == 2: # Pearson Distance
        return sim.getPearson()
    elif similarityMetric == 3: # Spearman Distance
        return sim.getPearson()
    elif similarityMetric == 4: # Cosine Distance
        return sim.getCosineMetric()

def compareNUsers(similarityMetric):
    ''' Returns n similar users '''
    userID = input('Please enter the user ID you want to compare: ')
    sim = nItems()
    sim.setUserID(userID)
    try:
        numElements = int(input('Please enter how many elements you would like to compare to: ')) 
    except ValueError:
        print('Please ensure value entered is an integer')
        return compareNUsers(similarityMetric)
    
    # Ensures no negative indexing 
    if numElements < 1:
        print('Please ensure number of elements exceeds zero')
        return compareNUsers(similarityMetric)
    else:
        if similarityMetric == 0: # Euclidean Distance
            return sim.getNSimilarItems('Euclidean',numElements)
        elif similarityMetric == 1: # Manhattan Distance
            return sim.getNSimilarItems('Manhattan',numElements)
        elif similarityMetric == 2: # Pearson Distance
            return sim.getNSimilarItems('Pearson',numElements)
        elif similarityMetric == 3: # Spearman Distance
            return sim.getNSimilarItems('Spearman',numElements)
        elif similarityMetric == 4: # Cosine Distance
            return sim.getNSimilarItems('Cosine',numElements)
       
def twoOrNSimilar(userOrBook):
    ''' Allows user to choose between comparing two or n items '''
    try:
        if userOrBook == 0:
            query = int(input('Please enter 0 to compare two books, or enter 1 to produce "n" similar items: '))
            if query == 0:
                return compare2Books()
            elif query == 1:
                return compareNBooks()
            else:
                print("Please ensure value entered is either 0 or 1 ")
                return twoOrNSimilar(userOrBook)
        else:
            query = int(input('Please enter 0 to compare two users, or enter 1 to produce "n" similar items: '))
            if query == 0:
                return getSimilarity(0)
            elif query == 1:
                return getSimilarity(1)
            else:
                print("Please ensure value entered is either 0 or 1 ")
                return twoOrNSimilar(userOrBook)              

    except ValueError:
        print("Please ensure the input is an integer")
        return twoOrNSimilar(userOrBook)
        
def bookOrUser():
    ''' Allows user to choose between comparing books and users '''
    try:
        print('Would you like to compare Books or Users')
        query = int(input('Books:0, Users:1 '))
        if query == 0:
            return twoOrNSimilar(0)
        if query == 1:
            return twoOrNSimilar(1) 
        else:
            print('Please ensure value entered is either 0 or 1')
            return bookOrUser()
    except ValueError:
        print('Please ensure value entered is an integer')
        return bookOrUser()

def main():
    print(bookOrUser())
    print('Would you like to compare more items?')
    runAgain = input('Yes:1, No:0 ')

    if runAgain == '1':
        return main()
    elif runAgain == '0':
            return 'Goodbye'
    else:
        print('Invalid input')
        print('Terminating program')


if __name__ == '__main__':
    main()
