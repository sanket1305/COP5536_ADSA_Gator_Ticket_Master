import sys
from pathlib import Path
from rbt import RedBlackTree
from binMinHeap import MinHeap
from binMaxHeap import MaxHeap

class GatorTicketMaster:
    # constructor
    # initialize variables for all data structures
    def __init__(self):
        self.availableSeats = None
        self.waitingList = None
        self.seatMapping = RedBlackTree()
    
    # function to handle initialize command
    def initialize(self, n):
        if not n.isdigit():
            out_file.write("Invalid input. Please provide a valid number of seats.\n")
        else:
            n = int(n)
            if n <= 0:
                out_file.write("Invalid input. Please provide a valid number of seats.\n")
            else:
                # created 1-n seats
                self.availableSeats = MinHeap(n)

                # initialize waiting list, which is empty at the start
                self.waitingList = MaxHeap()

                out_file.write(str(n) + " Seats are made available for reservation\n")

    # function to handle available command        
    def available(self):
        out_file.write("Total Seats Available : " + str(self.availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(self.waitingList.lengthofWaitlist()) + "\n")

    # function to handle reserve command
    def reserve(self, userId, priority):
        # check if seat is available
        isSeatAvailable = False
        if self.availableSeats.numberOfAvailableSeats():
            isSeatAvailable = True
        
        # if seat is not available, then put user in the waitlist
        # else assign the lowest available seat to the user
        if not isSeatAvailable:
            self.waitingList.insert(userId, priority)
            # print("jay shree ram")
            # print(self.waitingList.line)
            out_file.write("User " + str(userId) + " is added to the waiting list\n")
        else:
            # get lowest seat number available, which is unassigned
            seatId = self.availableSeats.removeMin()
            self.seatMapping.insert(userId, seatId)

            # uncomment below line if you want to see the whole assignment after each mapping
            # seatMapping.inorderTraversal(seatMapping.root)

            out_file.write("User " + str(userId) + " reserved seat " + str(seatId) + "\n")
    
    # function to handle cancel command
    def cancel(self, userId, seatId):
        # search for userId, as we have userId as key in RBT
        mapping = self.seatMapping.search(userId)

        # if there is no seat mapping for the user
        if mapping.userId == None:
            out_file.write("User " + str(userId)  + " has no reservation to cancel\n")
        elif mapping.seatId != seatId: # if user mapping exists but not with given seat ID
            out_file.write("User " + str(userId) + " has no reservation for seat " + str(seatId) + " to cancel\n")
        else:
            # user has the mapping to given seat
            # delete that mapping from RBT
            self.seatMapping.delete(userId)

            out_file.write("User " + str(userId) + " canceled their reservation\n")

            # insert the vacant seat back into the heap
            self.availableSeats.insert(mapping.seatId)

            # check if there is any user in waiting list
            # if there is, assign the released seat to the 1st user in waiting list
            if self.waitingList.line_size:
                temp = self.waitingList.removeMax()
                new_user = temp[2]
                new_user_priority = temp[0]
                self.reserve(new_user, new_user_priority)

    # function to handle exitWaitList command
    def exitWaitList(self, userId):
        if self.waitingList.removeUser(userId):
            out_file.write("User " + str(userId) + " is removed from the waiting list\n")
        else:
            out_file.write("User " + str(userId) + " is not in waitlist\n")

    # function to handle addSeats Command
    def addSeats(self, extraSeats):
        # check if given input is digit
        # if not print error msg in output file
        if extraSeats.isdigit():
            extraSeats = int(extraSeats)
            # if input for seatCount < 1, then it's invalid input
            if extraSeats < 1:
                out_file.write("Invalid input. Please provide a valid number of seats.\n")
            else:
                # add new seats to heap
                self.availableSeats.addSeats(extraSeats)

                out_file.write("Additional " + str(extraSeats) + " Seats are made available for reservation\n")

                # check if there is any user in waitlist
                if self.waitingList.line_size > 0:
                    # out_file.write("\n")
                    # while waitlist is not empty and seats are avialable
                    # keep removing user from waitlist and call reserve method for seat booking
                    while self.waitingList.line_size > 0 and self.availableSeats.numberOfAvailableSeats():
                        curr_user = self.waitingList.removeMax()
                        gatorTicketMaster.reserve(curr_user[2], curr_user[0])
                        # out_file.write("\n")
                        extraSeats -= 1
        else:
            out_file.write("Invalid input. Please provide a valid number of seats.\n")
    
    # function to handle releaseSeats call
    def releaseSeats(self, userId1, userId2):
        # for user in given range
        for userId in range(userId1, userId2 + 1):
            # check if userId is in waiting list, if it is remove it
            if not self.waitingList.removeUser(userId):
                # if userId is not in waiting list, check if it has seatMapping
                # if does not, then given userId was never introduced during current execution, so ingore it
                # if it does, then remove that seatMapping
                node = self.seatMapping.search(userId)
                if node.userId != None:
                    self.availableSeats.insert(node.seatId)
                    self.seatMapping.deleteNode(node)
        
        out_file.write("Reservations of the Users in the range [" + str(userId1) + ", " + str(userId2) + "] are released\n")

        while self.availableSeats.numberOfAvailableSeats() and self.waitingList.line_size:
            record = self.waitingList.removeMax()
            userId = record[2]
            priority = record[0]

            gatorTicketMaster.reserve(userId, priority)
            # out_file.write("\n")
    
    # function to handle printReservations call
    def printReservations(self):
        # get root node of RBT seat mapping
        node = self.seatMapping.root

        # array to store the mapping of seatId and userId
        arr = []

        # do inorder traversal to get all mappings
        def inorderMaster(node):
            if node is not None and node.userId is not None:
                inorderMaster(node.left)
                arr.append((node.seatId, node.userId))
                inorderMaster(node.right)

        # function call to inorder traversal method
        inorderMaster(node)
        arr.sort() # sorting array based on seatIds

        # print all mappings sorted by seatIds
        for index in range(len(arr)):
            # if index != 0:
            #     out_file.write("\n")
            out_file.write("Seat " + str(arr[index][0]) + ", User " + str(arr[index][1]) + "\n")
        # out_file.write("\n")
    
    # function to handle updatePriority call
    def updatePriority(self, userId, priority):
        # get waiting queue
        waiting_queue = self.waitingList.line
        # set user_found flag to false initially
        # if found, set it to true
        user_found = False

        for index in range(self.waitingList.line_size):
            # if user is found, set the flag, update the priority
            # call heapifyDown from that index, to update the heap
            if waiting_queue[index][2] == userId:
                user_found = True
                waiting_queue[index][0] = priority
                self.waitingList.heapifyUp(index)
        
        # print output based on user_found flag
        if user_found:
            out_file.write("User " + str(userId) + " priority has been updated to " + str(priority) + "\n")
        else:
            out_file.write("User " + str(userId) + " priority is not updated\n")

if __name__ == "__main__":
    # initialize the GetorTicketMaster class
    gatorTicketMaster = GatorTicketMaster()

    # get file name from arguments
    file_name = sys.argv[1]

    # check if given file_name is a file at current path
    if Path(file_name).is_file():

        # initialize input reader and output writer
        inp_file = open(file_name,"r+")
        out_file = open(file_name.replace(".txt", "") + "_output_file.txt","w+")

        print("Reading commands from " + f"{file_name}...")

        # retrive commands from input file
        commands = inp_file.readlines()
        num_commands = len(commands)

        # for each command, process arguments 
        # and call appropriate functions in GatorTicketMaster
        for i in range(0, num_commands):
            # print("command number", i)
            # if i != 0:
            #     out_file.write("\n")
            if commands[i][:10] == "Initialize":
                command = commands[i].split('(')
                command = command[1].split(')')
                n = command[0]
                
                gatorTicketMaster.initialize(n)
            elif commands[i][:9] == "Available":
                gatorTicketMaster.available()
            elif commands[i][:7] == "Reserve":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId = int(command[0])
                priority = int(command[1].strip())

                gatorTicketMaster.reserve(userId, priority)
            elif commands[i][:6] == "Cancel":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                seatId = int(command[0])
                userId = int(command[1].strip())

                gatorTicketMaster.cancel(userId, seatId)
            elif commands[i][:12] == "ExitWaitlist": 
                command = commands[i].split('(')
                command = command[1].split(')')
                userId = int(command[0])

                gatorTicketMaster.exitWaitList(userId)
            elif commands[i][:14] == "UpdatePriority":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId = int(command[0])
                new_priority = int(command[1].strip())

                gatorTicketMaster.updatePriority(userId, new_priority)
            elif commands[i][:8] == "AddSeats":
                command = commands[i].split('(')
                command = command[1].split(')')
                seat_count = command[0]

                gatorTicketMaster.addSeats(seat_count)
            elif commands[i][:17] == "PrintReservations":
                gatorTicketMaster.printReservations()
            elif commands[i][:12] == "ReleaseSeats":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId1 = command[0]
                userId2 = command[1].strip()
                
                if not userId1.isdigit() or not userId2.isdigit():
                    out_file.write("Invalid input. Please provide a valid range of users.\n")
                else:
                    userId1 = int(userId1)
                    userId2 = int(userId2)

                    if userId1 < 0 or userId2 < 0:
                        out_file.write("Invalid input. Please provide a valid range of users.\n")
                    else:
                        gatorTicketMaster.releaseSeats(userId1, userId2)
            elif commands[i][:4] == "Quit":
                out_file.write("Program Terminated!!")

                # To terminate the program
                break
            else:
                out_file.write("Invalid command\n")
        print("Output file " + file_name.replace(".txt", "") + "_output_file.txt" + " generated...")
    else:
        print(f"{file_name} does not exist")