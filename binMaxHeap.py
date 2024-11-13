import time

class MaxHeap:
    def __init__(self):
        # each element in line contains [priority, timestamp, userId]
        self.line = []   # to store all the elements
        self.size = 0                   # initial size of heap (i.e. 0)
    
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
        return self.line[self.getParentIndex(index)]
    
    # def leftChild(index)... to get left child value
    def leftChild(index):
        return self.line[self.getLeftChildIndex(index)]

    # def rightChild(index)... to get right child value
    def rightChild(index):
        return self.line[self.getRightChildIndex(index)]
    
    # function to swap the values at 2 indexes
    def swap(self, index1, index2):
        self.line[index1], self.line[index2] = self.line[index2], self.line[index1]
    
    # function to insert data into the heap
    def insert(self, userId, priority):
        # self.line[self.size] = data
        current_time_ns = time.time_ns()
        self.line.append([priority, current_time_ns, userId])
        self.size += 1
        # now we need to ensure that data is sorted in right position
        self.heapifyUp(self.size - 1)
    
    # function to sort the data in right position
    def heapifyUp(self, index):
        # check if parent exists
        # check if parent's priority is less than curr index, then we need swap
        # if parent's priority == index's priority, but parent came after index, then we need swap
        if(self.hasParent(index) and (self.parent(index)[0] < self.line[index][0] or (self.parent(index)[0] == self.line[index][0] and self.parent(index)[1] > self.parent(index)[1]))):
            self.swap(self.getParentIndex(index), index)
            self.heapifyUp(self.getParentIndex(index))
    
    # function to remove min element from the binary heap
    def removeMax(self):
        if self.size == 0:
            raise("Empty Heap")
        data = self.line[0]

        # replace the root, with the last element in heap array
        self.line[0] = self.line[self.size - 1]

        # reduce the size by 1, as we have removed min
        self.size -= 1

        # recursively call heap function to satisfy binary min heap property
        self.heapifyDown(0)
        return data
    
    # function to heapify from top to down
    def heapifyDown(self, index):
        # consider current idnex as largest
        largest = index

        # check if left child has smaller value
        if (self.hasLeftChild(index) and (self.line[largest][0] < self.leftChild(index)[0] or (self.line[largest][0] == self.leftChild(index)[0] and self.line[largest][1] > self.leftChild(index)[1]))):
            largest = self.getLeftChildIndex(index)
        
        # check if right child has smaller value
        if (self.hasRightChild(index) and (self.line[largest][0] < self.rightChild(index)[0] or (self.line[largest][0] == self.rightChild(index)[0] and self.line[largest][1] > self.rightChild(index)[1]))):
            largest = self.getRightChildIndex(index)
        
        # check if the largest is not current index
        # perform swap and recursivey call Heapify by traversing to bottom
        if largest != index:
            self.swap(index, largest)
            self.heapifyDown(largest)
    
    # function to return length of current waiting list
    def lengthofWaitlist(self):
        return self.size
    
    # function to remove a user from wait list
    # binary heap only ensures that top element is min/max
    # so searching for any other element in binary help would take O(n)
    # hence performing linear search directly
    def removeUser(self, userId):
        index = 0
        og_size = self.size
        while(index < self.size):
            if self.line[i][2] == userId:
                self.line[i] = self.line[self.size - 1]
                self.size -= 1
                self.heapifyDown(i)
                break
            index += 1
        if og_size == index:
            return False
        return True