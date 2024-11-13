import sys
from pathlib import Path
from my_rbt import RedBlackTree
from binMinHeap import MinHeap
from binMaxHeap import MaxHeap

class GatorTicketMaster:
    def __init__(self):
        self.availableSeats = None
        self.waitingList = None
        self.seatMapping = RedBlackTree()
    
    # function to handle initialize command
    def initialize(self, n):
        if not n.isdigit():
            out_file.write("Invalid input. Please provide a valid number of seats.")
        else:
            n = int(n)
            if n <= 0:
                out_file.write("Invalid input. Please provide a valid number of seats.")
            else:
                # created 1-n seats
                self.availableSeats = MinHeap(n)

                # initialize waiting list, which is empty at the start
                self.waitingList = MaxHeap()

                out_file.write(str(n) + " Seats are made available for reservation")

    # function to handle available command        
    def available(self):
        out_file.write("Total Seats Available : " + str(self.availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(self.waitingList.lengthofWaitlist()))

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
            out_file.write("User " + str(userId) + " is added to the waiting list")
        else:
            # get lowest seat numer available, which is unassigned
            seatId = self.availableSeats.removeMin()
            self.seatMapping.insert(userId, seatId)

            # uncomment below line if you want to see the whole assignment after each mapping
            # seatMapping._inorder_traversal(seatMapping.root)

            out_file.write("User " + str(userId) + " reserved seat " + str(seatId))
    
    # function to handle cancel command
    def cancel(self, userId, seatId):
        # search for userId, as we have userId as key in RBT
        mapping = self.seatMapping.search(userId)

        # if there is no seat mapping for the user
        if mapping.userId == None:
            out_file.write("User " + str(userId)  + " has no reservation to cancel")
        elif mapping.seatId != seatId: # if user mapping exists but not with given seat ID
            out_file.write("User " + str(userId) + " has no reservation for seat " + str(seatId) + " to cancel")
        else:
            # user has the mapping to given seat
            # delete that mapping from RBT
            self.seatMapping.delete(userId)

            out_file.write("User " + str(userId) + " canceled their reservation")

            # insert the vacant seat back into the heap
            self.availableSeats.insert(mapping.seatId)

            # check if there is any user in waiting list
            # if there is, assign the released seat to the 1st user in waiting list
            if self.waitingList.size:
                temp = self.waitingList.removeMax()
                new_user = temp[2]
                new_user_priority = temp[0]
                self.reserve(new_user, new_user_priority)

            # self.seatMapping._inorder_traversal(self.seatMapping.root)  

    # function to handle exitWaitList command
    def exitWaitList(self, userId):
        if self.waitingList.removeUser(userId):
            out_file.write("User " + userId + " is removed from the waiting list")
        else:
            out_file.write("User " + userId + " is not in waitlist")

    # function to handle addSeats Command
    def addSeats(self, extraSeats):
        # check if given input is digit
        # if not print error msg in output file
        if seat_count.isdigit():
            seat_count = int(seat_count)
            # if input for seatCount < 1, then it's invalid input
            if seat_count < 1:
                out_file.write("Invalid input. Please provide a valid number of seats.")
            else:
                # add new seats to heap
                self.availableSeats.addSeats(seat_count)

                # check if there is any user in waitlist
                if self.waitingList.size > 0:
                    # while waitlist is not empty and seats are avialable
                    # keep removing user from waitlist and call reserve method for seat booking
                    while self.waitingList.size > 0 and self.availableSeats.isSeatAvailable():
                        curr_user = self.waitingList.removeMax()
                        gatorTicketMaster.reserve(curr_user[2], curr_user[0])
                        seat_count -= 1
                
                # at this stage either the waitlist is empty or seats are full.
                # if seats are not full, then print the msg of seats available
                if seat_count:
                    out_file.write("Additional " + str(seat_count) + " Seats are made available for reservation")
        else:
            out_file.write("Invalid input. Please provide a valid number of seats.")

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
            if i != 0:
                out_file.write("\n")
            if commands[i][:10] == "Initialize": # completed
                command = commands[i].split('(')
                command = command[1].split(')')
                n = command[0]
                
                gatorTicketMaster.initialize(n)
            elif commands[i][:9] == "Available": # completed
                gatorTicketMaster.available()
            elif commands[i][:7] == "Reserve": # completed
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
                userId = command[0]
                new_priority = command[1].strip()
                out_file.write("Updating priority for userId: " + userId + " New priority is: " + new_priority)
            elif commands[i][:8] == "AddSeats":
                command = commands[i].split('(')
                command = command[1].split(')')
                seat_count = command[0]

                gatorTicketMaster.addSeats(seat_count)
            elif commands[i][:17] == "PrintReservations":
                out_file.write("Printing reservations...")
            elif commands[i][:12] == "ReleaseSeats":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId1 = command[0]
                userId2 = command[1].strip()
                out_file.write("Releasing seats in range: " + userId1 + " : " + userId2)
            elif commands[i][:4] == "Quit":
                out_file.write("Program Terminated!!")
            else:
                out_file.write("Invalid command")
        print()
    else:
        print(f"{file_name} does not exist")