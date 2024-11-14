import time

class MaxHeap:
    # constructor
    def __init__(self):
        # each element in line contains [priority, timestamp, userId]
        self.line = []   # to store all the elements
        self.line_size = 0                   # initial line_size of heap (i.e. 0)
    
    # function to return length of current waiting list
    def lengthofWaitlist(self):
        return self.line_size
    
    # function to exchangeIndexValues the values at 2 indexes
    def exchangeIndexValues(self, index1, index2):
        self.line[index1], self.line[index2] = self.line[index2], self.line[index1]
    
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
        if childIndex < self.line_size:
            return True
        
        # if calculated left child index < 0 that means 
        # the node does not have left child
        return False
    
    # function to check if index has right child
    def checkRightChild(self, index):
        childIndex = self.calculateRightChildIndex(index)
        if childIndex < self.line_size:
            return True
        # if calculated right child index < 0 that means 
        # the node does not have right child
        return False
    
    # function to get parent value
    def parent(self, index):
        return self.line[self.calculateParentIndex(index)]
    
    # function to get left child value
    def leftChild(self, index):
        return self.line[self.calculateLeftChildIndex(index)]

    # function to get right child value
    def rightChild(self, index):
        return self.line[self.calculateRightChildIndex(index)]
    
    # function to sort the data in right position
    def heapifyUp(self, index):
        # check if parent exists
        # check if parent's priority is less than curr index, then we need exchangeIndexValues
        # if parent's priority == index's priority, but parent came after index, then we need exchangeIndexValues
        if(self.checkParent(index) and (self.parent(index)[0] < self.line[index][0] or (self.parent(index)[0] == self.line[index][0] and self.parent(index)[1] > self.line[index][1]))):
            self.exchangeIndexValues(self.calculateParentIndex(index), index)
            self.heapifyUp(self.calculateParentIndex(index))
    
    # function to heapify from top to down
    def heapifyDown(self, index):
        # consider current idnex as largest
        largest = index

        # check if left child has smaller value
        if (self.checkLeftChild(index) and (self.line[largest][0] < self.leftChild(index)[0] or (self.line[largest][0] == self.leftChild(index)[0] and self.line[largest][1] > self.leftChild(index)[1]))):
            largest = self.calculateLeftChildIndex(index)
        
        # check if right child has smaller value
        if (self.checkRightChild(index) and (self.line[largest][0] < self.rightChild(index)[0] or (self.line[largest][0] == self.rightChild(index)[0] and self.line[largest][1] > self.rightChild(index)[1]))):
            largest = self.calculateRightChildIndex(index)
        
        # check if the largest is not current index
        # perform exchangeIndexValues and recursivey call Heapify by traversing to bottom
        if largest != index:
            self.exchangeIndexValues(index, largest)
            self.heapifyDown(largest)
    
    # function to insert data into the heap
    def insert(self, userId, priority):
        # get current timestamp in nano seconds
        current_time_ns = time.time_ns()

        # add the new user to waitlist
        self.line.append([priority, current_time_ns, userId])
        self.line_size += 1
        
        # now we need to ensure that data is sorted in right position
        self.heapifyUp(self.line_size - 1)
    
    # function to remove min element from the binary heap
    def removeMax(self):
        # debugger to check if invalid removeMax has been called
        if self.line_size == 0:
            print("Empty Heap")
        data = self.line[0]

        # replace the root, with the last element in heap array
        self.line[0] = self.line[self.line_size - 1]

        # reduce the line_size by 1, as we have removed min
        self.line_size -= 1
        self.line.pop(-1)

        # recursively call heap function to satisfy binary min heap property
        self.heapifyDown(0)
        return data
    
    # function to remove a user from wait list
    # binary heap only ensures that top element is min/max
    # so searching for any other element in binary help would take O(n)
    # hence performing linear search directly
    def removeUser(self, userId):
        index = 0
        og_size = self.line_size
        while(index < self.line_size):
            if self.line[index][2] == userId:
                self.line[index] = self.line[self.line_size - 1]
                self.line_size -= 1
                self.heapifyDown(index)
                break
            index += 1
        
        # below condition indicates that we reached end of line
        # but the user was not found in the queue
        # so return False, as user has not been removed
        if og_size == index:
            return False
        return True
