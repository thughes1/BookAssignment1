import load_dataset_module
from similarity_module import SimilarityUsers as sUsers
from similarity_module import SimilarityBooks as sBooks
from similarity_module import NSimilarItems as nItems

def getSimilarity(comparisonType):
    print('Please select the distance metric desired')
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

def compare2Books():
    book1 = input('Please enter the ISBN of the first book: ')
    book2 = input('Please enter the ISBN of the second book: ')
    sim = sBooks() 
    sim.setBook1(book1)
    sim.setBook2(book2)
    #0345339711
    #059035342X
    return sim.getSimilarity()

def compareNBooks():
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
    userID = input('Please enter the user ID you want to compare: ')
    sim = nItems()
    sim.setUserID(userID)
    try:
        numElements = int(input('Please enter how many elements you would like to compare to: ')) # Ensure no negative indexing
    except ValueError:
        print('Please ensure value entered is an integer')
        return compareNUsers(similarityMetric)

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
    try:
        if userOrBook == 0:
            query = int(input('Please enter 0 to compare two books, or enter 1 to produce "n" similar items: '))
            if query == 0:
                return compare2Books()
            elif query == 1:
                return compareNBooks()
            else:
                print("Please ensure value entered is either 0 or 1: ")
                return twoOrNSimilar(userOrBook)
        else:
            query = int(input('Please enter 0 to compare two users, or enter 1 to produce "n" similar items: '))
            if query == 0:
                return getSimilarity(0)
            elif query == 1:
                return getSimilarity(1)
            else:
                print("Please ensure value entered is either 0 or 1: ")
                return twoOrNSimilar(userOrBook)              

    except ValueError:
        print("Please ensure the input is an integer")
        return twoOrNSimilar(userOrBook)
        
def bookOrUser():
    try:
        query = int(input('If you would like to compare Books enter 0, for Users enter 1: '))
        if query == 0:
            return twoOrNSimilar(0)
        if query == 1:
            return twoOrNSimilar(1) 
        else:
            print('Please ensure value entered is either 0 or 1: 0')
            return bookOrUser()
    except ValueError:
        print('Please ensure value entered is an integer')
        return bookOrUser()

def main():
    # Questions are split into individual functions, such that 
    # they can be recursively called without having to start the questions again
    print(bookOrUser())
    #print(compareNBooks())
    runAgain = input("Would you like to compare more items? Press 1 for 'yes' and 0 for 'no' ")
    try:
        if runAgain == 1:
            return main()
        elif runAgain == 0:
            print('Goodbye')
        else:
            pass
    except ValueError:
        pass

if __name__ == '__main__':
    main()
