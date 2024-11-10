class MinHeap:
    def __init__(self, maxSize):
        self.storage = [0] * maxSize    # to store all the elements
        self.maxSize = maxSize          # maximum capacity of the heap
        self.size = 0                   # initial size of heap (i.e. 0)
    
    # function to get parent index
    def getParentIndex(self, index):
        return (index - 1)//2
    
    # function to get left child
    def getLeftChild(self, index):
        return 2*index + 1
    
    # function to get right child
    def getRightChild(self, index):
        return 2*index + 2
    
    # function to check if current index has parent
    def hasParent(self, index):
        parentIndex = self.getParentIndex(index)
        if parentIndex >= 0:
            return True
        return False
    
    # function to check if index has left child
    def hasLeftChild(self, index):
        childIndex = self.getLeftChild(index)
        if childIndex < self.size:
            return True
        return False
    
    # function to check if index has right child
    def has_right_child(self, index):
        childIndex = self.getRightChild(index)
        if childIndex < self.size:
            return True
        return False
    
    # def parent(index)... to get parent value
    def parent(self, index):
        return self.storage[index]
    # def leftChild(index)... to get left child value
    # def rightChild(index)... to get right child value

    # function to check if the heap is full
    def isFull(self):
        if self.size == self.maxSize:
            return True
        return False
    
    # function to swap the values at 2 indexes
    def swap(self, index1, index2):
        self.storage[index1], self.storage[index2] = self.storage[index2], self.storage[index1]
    
    # function to insert data into the heap
    def insert(self, data):
        if self.isFull():
            raise("Heap is Full")
        self.storage[self.size] = data
        self.size += 1
        # now we need to ensure that data is sorted in right position
        self.heapifyUp()
    
    # function to sort the data in right position
    def heapifyUp(self):
        index = self.size - 1
        # while(self.hasParent[index] and self.)