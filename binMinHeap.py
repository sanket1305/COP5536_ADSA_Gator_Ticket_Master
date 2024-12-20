class MinHeap:
    def __init__(self, maxSize):
        self.seats = []
        for i in range(1, maxSize + 1):
            self.seats.append(i)
        self.maxSize = maxSize          # maximum capacity of the heap
        self.size = maxSize                   # initial size of heap (i.e. 0)

    # function to check if the heap is full
    # as we have fixed number of seats
    # this function won't be there in waitlist heap
    # as waitlist can be as long as it can
    def isFull(self):
        if self.size == self.maxSize:
            return True
        return False

    # function to print the list of available seats
    def numberOfAvailableSeats(self):
        return self.size
    
    # function to exchangeIndexValues the values at 2 indexes
    def exchangeIndexValues(self, index1, index2):
        self.seats[index1], self.seats[index2] = self.seats[index2], self.seats[index1]
    
    # function to get parent index
    def calculateParentIndex(self, index):
        return (index - 1)//2
    
    # function to get left child
    def calculateLeftChildIndex(self, index):
        return 2*index + 1
    
    # function to get right child
    def calculateRightChildIndex(self, index):
        return 2*index + 2
    
    # function to check if current index has parent
    def checkParent(self, index):
        parentIndex = self.calculateParentIndex(index)
        if parentIndex >= 0:
            return True
        
        # if calculated parent index < 0 that means 
        # the node does not have parent
        return False
    
    # function to check if index has left child
    def checkLeftChild(self, index):
        childIndex = self.calculateLeftChildIndex(index)
        if childIndex < self.size:
            return True
        
        # if calculated left child index < 0 that means 
        # the node does not have left child
        return False
    
    # function to check if index has right child
    def checkRightChild(self, index):
        childIndex = self.calculateRightChildIndex(index)
        if childIndex < self.size:
            return True
        
        # if calculated right child index < 0 that means 
        # the node does not have right child
        return False
    
    # def parent(index)... to get parent value
    def parent(self, index):
        return self.seats[self.calculateParentIndex(index)]
    
    # def leftChild(index)... to get left child value
    def leftChild(self, index):
        return self.seats[self.calculateLeftChildIndex(index)]

    # def rightChild(index)... to get right child value
    def rightChild(self, index):
        return self.seats[self.calculateRightChildIndex(index)]

    # function to sort the data in right position
    def heapifyUp(self, index):
        # keep comparing values with parent (until we reach the root)
        # perform swapping if required (to satisfy mean Heap property)
        # move one level up
        if(self.checkParent(index) and self.parent(index) > self.seats[index]):
            self.exchangeIndexValues(self.calculateParentIndex(index), index)
            self.heapifyUp(self.calculateParentIndex(index))
    
    # function to heapify from top to down
    def heapifyDown(self, index):
        # consider current idnex as smallest
        smallest = index

        # check if left child has smaller value
        if (self.checkLeftChild(index) and self.seats[smallest] > self.leftChild(index)):
            smallest = self.calculateLeftChildIndex(index)
        
        # check if right child has smaller value
        if (self.checkRightChild(index) and self.seats[smallest] > self.rightChild(index)):
            smallest = self.calculateRightChildIndex(index)
        
        # check if the smallest is not current index
        # perform exchangeIndexValues and recursivey call Heapify by traversing to bottom
        if smallest != index:
            self.exchangeIndexValues(index, smallest)
            self.heapifyDown(smallest)

    # function to insert data into the heap
    def insert(self, data):
        if self.isFull():
            print("Heap is Full")
        
        # insert new/vacant seatId into heap at the end
        self.seats.append(data)
        self.size += 1

        # now we need to ensure that data is sorted in right position
        self.heapifyUp(self.size - 1)
    
    # function to remove min element from the binary heap
    def removeMin(self):
        # debugger to check if there is invalid remove operation called
        if self.size == 0:
            print("Empty Heap")
        data = self.seats[0]

        # replace the root, with the last element in heap array
        self.seats[0] = self.seats[self.size - 1]

        # reduce the size by 1, as we have removed min
        self.size -= 1
        del self.seats[self.size] # remove last element

        # recursively call heap function to satisfy binary min heap property
        self.heapifyDown(0)
        return data
    
    # function to add seats
    def addSeats(self, extraSeats):
        # existing seats will be having smaller IDs than new ones
        # this is mean heap
        # so no new seatId would go up the tree
        # hence directly appending the new seats into the array
        for seat in range(self.maxSize + 1, self.maxSize + extraSeats + 1):
            self.seats.append(seat)
        self.maxSize += extraSeats
        self.size += extraSeats
