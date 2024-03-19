#Cuckoo Hash

#"I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.”

import random
from BitHash import *
import pytest

class Datum(object):
    def __init__(self, k, d):
        self.key  = k
        self.data = d
        
class HashTab(object):
    def __init__(self, size):
        self.__hashArray1 = [None] * size
        self.__numKeys1 = 0
        self.__bitHash1 = 0
        
        self.__hashArray2 = [None] * size
        self.__numKeys2 = 0 #will be used for testing
        self.__bitHash2 = 1
        
    # return current number of keys in table 1   
    def len1(self): 
        return self.__numKeys1
    
    #This method will be used to ensure that the amounts
    #in both hashtables equals the total
    
    # return current number of keys in table 2   
    def len2(self): 
        return self.__numKeys2
    
    def totalKeys(self):
        return self.__numKeys1 + self.__numKeys2
    
    #Check size will determine if we need to grow the hashtables
    def checkSize(self):
        #If the hashtables were empty, create hashtables that hold at least one key data pair
        if len(self.__hashArray1) == 0:
            self.__hashArray1 = [None]
            self.__hashArray2 = [None]
        
        #if hash1 is 1/2 full, grow it
        if self.__numKeys1 > len(self.__hashArray1) // 2:
            
            self.growHashTables()
        
##IsCorrect
    #isCorrect will be used for testing
    #this method returns false if any key data pair is not in
    #its correct place. If all is good, it returns true
    def isCorrect(self):
        #Loop through array 1
        for i in range(0, len(self.__hashArray1)):
            if self.__hashArray1[i] != None:
                keyInBucket1 = self.__hashArray1[i].key
                
                #Now hash the key to make sure it is where it is supposed to be
                bucketIn1 = BitHash(keyInBucket1, self.__bitHash1) % len(self.__hashArray1)
                if bucketIn1 != i:
                    return False
                
        #Loop through array 2
        for i in range(0, len(self.__hashArray2)):
            if self.__hashArray2[i] != None:
                keyInBucket2 = self.__hashArray2[i].key
                
                #Now hash the key to make sure it is where it is supposed to be
                bucketIn2 = BitHash(keyInBucket2, self.__bitHash2) % len(self.__hashArray1)
                if bucketIn2 != i:
                    return False
                                
        #return True if everything is where it is supposed to be    
        return True 
    
##Confirm Amounts
    #confirmAmounts will be used for testing to ensure that all keys are
    #accounted for and the total keys = # of keys in Hash1 + # of keys in Hash2
    def confirmAmounts(self):
        if self.len1() + self.len2() != self.totalKeys():
            return False
        
        return True
        
##growHashTables
    #growHashTables takes in a growthFactor (this is helpful if we will need to grow 
    #multiple times). This method returns true upon success and false if unsuccessful.
    #Based on aggressive testing, this method is successful.
    
    def growHashTables(self, growthFactor = 2):
    
        #Hold onto both of the arrays to loop through
        temp1 = self.__hashArray1
        temp2 = self.__hashArray2
        
        #Increase the bitHash number        
        self.__bitHash1 += 1
        self.__bitHash2 += 1
        
        #Double the size of the current hashtabs
        self.__hashArray1 = [None] * (growthFactor * len(temp1))
        self.__hashArray2 = [None] * (growthFactor * len(temp2))
        
        #loop through the old hashtable which is being held in temp1
        for i in range(0, len(temp1)):
            #check if there is something in this bucket
            if temp1[i] != None:
                #Use insert to insert into self.__hashArray1 or self.__hashArray2
                evictedMostRecently = self.__insertHelper(temp1[i].key,temp1[i].data)
                if evictedMostRecently != None:
                    #If the grow failed, meaning the insert returned a tuple instead of None, return False
                    return False                    
                
        #loop through the other old hashtable which is being held in temp2
        for i in range(0, len(temp2)):
            #check if there is something in this bucket
            if temp2[i] != None:
                #Use insert to insert into self.__hashArray1 or self.__hashArray2
                evictedMostRecently = self.__insertHelper(temp2[i].key,temp2[i].data)
                if evictedMostRecently != None:
                    #If the grow failed, meaning the insert returned a tuple instead of None, return False
                    return False
        
        #when successful return true
        return True
        
    
                
##Insert helper
    #Insert helper attempts to insert/evict and then reinsert maxLoops
    #amount of times. If successful, it returns None. If unsuccessful
    #it returns the most recently evicted key data pair so that we can
    #reattempt after growing and changing the bitHash number.
    def __insertHelper(self, k, d):
        
        maxLoops = 10
        curLoops = 0
        
        #create a datum with they key data pair to insert
        d = Datum(k, d)        
        
        #Prevent an infite loop, make sure the datum has data
        #and we haven't reached maxLoops
        while d.data and curLoops < maxLoops:
            
            #increment the loop
            curLoops += 1
            
            #Find its location in both of the hashtables
            #using their respective hash functions
            bucketIn1 = BitHash(d.key, self.__bitHash1) % len(self.__hashArray1)
            
            #Now we have to check if there is a datum already inside of hashtable self
            #Or if the bucket already holds this key, replace it
            if self.__hashArray1[bucketIn1] == None or \
               self.__hashArray1[bucketIn1].key == d.key:
                
                #Only increment if this isn't a key replacement
                if self.__hashArray1[bucketIn1] == None:
                    self.__numKeys1 += 1                
                        
                #Put the new datum or replacement in
                self.__hashArray1[bucketIn1] = d
                
                #If successful then return None
                return None
                
            #If there is something already in the bucket...
            elif self.__hashArray1[bucketIn1] != None:
                
                #Hold onto what is currently in the bucket
                temp1 = self.__hashArray1[bucketIn1]
                #Put the new datum in
                self.__hashArray1[bucketIn1] = d
                
                #No need to adjust numkeys
                
                #Now find a place for temp1 in the other hashtable
                bucketIn2 = BitHash(temp1.key, self.__bitHash2) % len(self.__hashArray2)
                
                #If it is empty or holds the same data, place it there
                if self.__hashArray2[bucketIn2] == None or \
                   self.__hashArray2[bucketIn2].key == temp1.key:
                    
                    #Only increment if this isn't a key replacement
                    if self.__hashArray2[bucketIn2] == None:
                        self.__numKeys2 += 1 
                        
                    self.__hashArray2[bucketIn2] = temp1
                    
                    #If successful then return None
                    return None                    
                    
                #But if it is already full...
                elif self.__hashArray2[bucketIn2] != None:
                    #evict and run the loop again and try to insert
                    #the most recently evicted one
                    
                    #Hold onto what is currently in the bucket
                    temp2 = self.__hashArray2[bucketIn2]
                    #Put the new datum in
                    self.__hashArray2[bucketIn2] = temp1
                    
                    d = temp2
                    
        #if we fell out of the while loop
        #return the key data pair that we are left with
        #we will have to rehash and try to insert again
        return (d.key, d.data)
    
##Insert
    #Insert takes in a key,data pair and uses a helper method to do the actual
    #insert process. Insert will return true once successful and false if unsuccessful
    #Insert will attempt the process of insert/eviction and growth maxLoops=3 times
    def insert(self, k, d):
        maxLoops = 3
        curLoops = 0
        growthFactor = 2
        
        #Check the size of the hashtables
        #if they need to be grown then it will grow
        #in that function
        self.checkSize()
            
        
        #Allow this process to happen maxLoops times
        while curLoops < maxLoops:
            
            #Attempt insert
            evictedMostRecently = self.__insertHelper(k, d)                
            
            #If successful, insert returns True
            if evictedMostRecently == None:
                return True
                
            #If the insert wasn't successful
            elif evictedMostRecently != None:
                #Grow the hashtables
                self.growHashTables(growthFactor)
                
                #Then try again, key is at index 0, data is at index 1
                k = evictedMostRecently[0]
                d = evictedMostRecently[1]
                
                #increment curLoops
                curLoops += 1
                #increase the growth factor each time
                growthFactor += 2                
            
        #If we made it here, the insert was unsuccessful after
        #many attempts and something is wrong
        print("INSERT FAILED", flush = True)
        return False

##FindHelper
    #FindHelper returns the data and bucket index of the key that is being searched for
    #this return will allow delete to be more efficient (since the bucket index is given).
    #Find returns None if the key was not found.
    def __findHelper(self, k):
       
        #Find the locations
        bucketIn1 = BitHash(k, self.__bitHash1) % len(self.__hashArray1)
        bucketIn2 = BitHash(k, self.__bitHash2) % len(self.__hashArray2)
        
        #Check hashtable self
        if self.__hashArray1[bucketIn1] != None and self.__hashArray1[bucketIn1].key == k:
            #If found in self, return is data and it's bucket index
            return self.__hashArray1[bucketIn1].data , bucketIn1
        
        #Check hashtable 2
        elif self.__hashArray2[bucketIn2] != None and self.__hashArray2[bucketIn2].key == k:
            #If found in 2, return is data and it's bucket index
            return self.__hashArray2[bucketIn2].data , bucketIn2
        
        #Not found, so return false
        return None
    
##Find
    #Find returns the data of the key that is being searched for
    #Find returns None if the key was not found.
    def find(self, k):
        
        data = self.__findHelper(k)
        if data == None:
            #Not found, so return false
            return None
        #return the data which is in the tuple that was returned
        return data[0]
        
##Delete
    #Delete uses the findHelper method to check if the key given is there and if it is
    #it uses the bucket index given to delete the key
    #If delete is unsuccessful for some reason or because it was not there,
    #it returns False.
    #Returns true when successful
    def delete(self, k):
        
        #Check if it is there, if it is not then return False
        if self.__findHelper(k) == None:
            return False
        
        #If find returned a tuple, it is there
        elif self.__findHelper(k) != None:
            #Get the index from the tuple that was returned
            location = self.__findHelper(k)[1]
            
            #Check 1
            if self.__hashArray1[location] != None and self.__hashArray1[location].key == k:
                #Delete and return True
                self.__hashArray1[location] = None
                #Decrement the numKeys
                self.__numKeys1 -= 1
                return True
            
            #Check 2
            elif self.__hashArray2[location] != None and self.__hashArray2[location].key == k:
                #Delete and return True
                self.__hashArray2[location] = None
                #Decrement the numKeys
                self.__numKeys2 -= 1
                return True
            
        #Unsuccessful delete
        return False
        
#This function creates a cuckoo hash with random key data pairs
#the size is how large to make the array and the insertAmount is
#how many key data pairs you would like to be inserted.
def createRandomCuckoo(size, insertAmount):
    # create a hash table with an initially small number of buckets
    h = HashTab(size)
    # Now insert size key/data pairs
    for i in range(insertAmount): 
        key = random.random()
        data = random.random()
        h.insert(key, data)  
        
    #h.display()
    return h

####################################################################
##Testing
#Check an empty cuckoohash is still a cuckoohash
def test_isCuckooEmpty():
    h = createRandomCuckoo(0,0)
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
#Try creating a random cuckoohash
def test_isCuckooRandom():
    h = createRandomCuckoo(6,1)
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True

#Insert one item and continue to make sure 
#that amounts are true and it is still a cuckoohash
def test_insertOne():
    h = createRandomCuckoo(10,0)
    totalBeforeInsert = h.totalKeys()
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,5)
    
    #Should have one more key now
    assert h.totalKeys() == totalBeforeInsert + 1
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True   

#Create a random cuckoohash and insert a lot
def test_insertMany():
    h = createRandomCuckoo(300,50)
    
    for i in range(100): 
        key = random.randint(1,100)
        data = random.randint(1,100)
        h.insert(key, data)
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True        
    
#Confirm that an insert of the same key is overwritten
def test_insertRepeat():
    h = createRandomCuckoo(4,0)
    totalBeforeInsert = h.totalKeys()
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,5)
    
    #Should have one more key now
    assert h.totalKeys() == totalBeforeInsert + 1
    
    #Try to insert the same key
    h.insert(6,7)
    
    #Should have the same amount of keys as before the repeated insert key
    assert h.totalKeys() == totalBeforeInsert + 1

    assert h.isCorrect() == True
    assert h.confirmAmounts() == True

#Delete a key that is there
def test_deleteThere():
    h = createRandomCuckoo(10,0)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,7)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True    
    
    assert h.delete(6) == True
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True    
    
#Delete a key that is not there
def test_deleteNotThere():
    h = createRandomCuckoo(10,0)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,7)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    assert h.delete(8) == False
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True   
    
#Insert and then delete many key data pairs
def test_aggressiveDelete():
    h = createRandomCuckoo(30,0)
    
    for i in range(100): 
        key = random.random()
        data = random.random()
        h.insert(key, data)
        
        #make sure it was deleted
        assert h.delete(key) == True
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True    

#Find a key that is for sure there
def test_findThere():
    h = createRandomCuckoo(10,0)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,7)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    #Find returns the data, here the data should be 7
    assert h.find(6) == 7
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True 
    
#Insert and find many random key data pairs
def test_aggressiveFind():
    h = createRandomCuckoo(30,0)
    
    for i in range(100): 
        key = random.random()
        data = random.random()
        h.insert(key, data)
        
        #make sure it is there and matches the data pair
        assert h.find(key) == data
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True

#Try to find keys that are not there
def test_findNotThere():
    h = createRandomCuckoo(10,0)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    h.insert(6,7)
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True
    
    #This will not be found, therefore it will return None
    assert h.find(8) == None
    
    assert h.isCorrect() == True
    assert h.confirmAmounts() == True   
    
#Test that growHash works by overloading the current cuckoohash
def test_mustGrow():
    #Force grow by inserting more than 30 key data pairs
    h = createRandomCuckoo(30,0)
    
    for i in range(20): 
        key = random.randint(1,100)
        data = random.randint(1,100)
        h.insert(key, data)
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True

#Test growth multiple times by forcing multiple grows
def test_growMultipleTimes():
    #Force grow multiple times by inserting more than 3 times the orignial size
    h = createRandomCuckoo(30,0)
    
    for i in range(100): 
        key = random.random()
        data = random.random()
        h.insert(key, data)
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True
    
#Start from a completely empty cuckoohash and add 1,000 to make sure that insert
#and grow are functioning very well
def test_growFromNothing():
    #Start empty and aggressively force it to grow
    h = createRandomCuckoo(0,0)
    
    for i in range(1000): 
        key = random.random()
        data = random.random()
        h.insert(key, data)
        
        assert h.isCorrect() == True
        assert h.confirmAmounts() == True

pytest.main(["-v", "-s", "Cuckoo Hash.py"])