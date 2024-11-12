class MinHeap:
    def __init__(self, maxSize):
        self.seats = []
        for i in range(1, maxSize + 1):
            self.seats.append(i)
        # print("hello", self.seats)
        # self.seats = [0] * maxSize    # to store all the elements
        self.maxSize = maxSize          # maximum capacity of the heap
        self.size = maxSize                   # initial size of heap (i.e. 0)
    
    # function to get parent index
    def getParentIndex(self, index):
        return (index - 1)//2
    
    # function to get left child
    def getLeftChildIndex(self, index):
        return 2*index + 1
    
    # function to get right child
    def getRightChildIndex(self, index):
        return 2*index + 2
    
    # function to check if current index has parent
    def hasParent(self, index):
        parentIndex = self.getParentIndex(index)
        if parentIndex >= 0:
            return True
        return False
    
    # function to check if index has left child
    def hasLeftChild(self, index):
        childIndex = self.getLeftChildIndex(index)
        if childIndex < self.size:
            return True
        return False
    
    # function to check if index has right child
    def hasRightChild(self, index):
        childIndex = self.getRightChildIndex(index)
        if childIndex < self.size:
            return True
        return False
    
    # def parent(index)... to get parent value
    def parent(self, index):
        return self.seats[self.getParentIndex(index)]
    
    # def leftChild(index)... to get left child value
    def leftChild(self, index):
        return self.seats[self.getLeftChildIndex(index)]

    # def rightChild(index)... to get right child value
    def rightChild(self, index):
        return self.seats[self.getRightChildIndex(index)]

    # function to check if the heap is full
    def isFull(self):
        if self.size == self.maxSize:
            return True
        return False
    
    # function to swap the values at 2 indexes
    def swap(self, index1, index2):
        self.seats[index1], self.seats[index2] = self.seats[index2], self.seats[index1]
    
    # function to insert data into the heap
    def insert(self, data):
        if self.isFull():
            raise("Heap is Full")
        # print(len(self.seats), self.size)
        self.seats.append(data)
        self.size += 1
        # now we need to ensure that data is sorted in right position
        self.heapifyUp(self.size - 1)
    
    # function to sort the data in right position
    def heapifyUp(self, index):
        if(self.hasParent(index) and self.parent(index) > self.seats[index]):
            self.swap(self.getParentIndex(index), index)
            self.heapifyUp(self.getParentIndex(index))
    
    # function to remove min element from the binary heap
    def removeMin(self):
        if self.size == 0:
            raise("Empty Heap")
        data = self.seats[0]

        # replace the root, with the last element in heap array
        self.seats[0] = self.seats[self.size - 1]

        # reduce the size by 1, as we have removed min
        self.size -= 1
        del self.seats[self.size] # remove last element

        # recursively call heap function to satisfy binary min heap property
        self.heapifyDown(0)
        return data
    
    # function to heapify from top to down
    def heapifyDown(self, index):
        # consider current idnex as smallest
        smallest = index

        # check if left child has smaller value
        if (self.hasLeftChild(index) and self.seats[smallest] > self.leftChild(index)):
            smallest = self.getLeftChildIndex(index)
        
        # check if right child has smaller value
        if (self.hasRightChild(index) and self.seats[smallest] > self.rightChild(index)):
            smallest = self.getRightChildIndex(index)
        
        # check if the smallest is not current index
        # perform swap and recursivey call Heapify by traversing to bottom
        if smallest != index:
            self.swap(index, smallest)
            self.heapifyDown(smallest)
    
    # function to print the list of available seats
    def numberOfAvailableSeats(self):
        return self.size