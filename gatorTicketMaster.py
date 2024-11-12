# scenarios remaining: if for a person, priority is updated, should we update its timestamp as well?

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

    def initialize(self, n):
        if not n.isdigit():
            out_file.write("Invalid input. Please provide a valid number of seats.")
        else:
            n = int(n)
            # created 1-n seats
            self.availableSeats = MinHeap(n)

            # initialize waiting list, which is empty at the start
            self.waitingList = MaxHeap()

            out_file.write(str(n) + " Seats are made available for reservation")
            # print(availableSeats.storage)
        
    def available(self):
        out_file.write("Total Seats Available : " + str(self.availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(self.waitingList.lengthofWaitlist()))

    def reserve(self, userId, priority):
        # check if seat is available
        isSeatAvailable = False
        if self.availableSeats.numberOfAvailableSeats():
            isSeatAvailable = True
        
        # if seat is not avilable, then put user in the waitlist
        # else assign the lowest availablt seat to the user
        if not isSeatAvailable:
            self.waitingList.insert(userId, priority)
            # print(waitingList.line)
            out_file.write("User " + str(userId) + " is added to the waiting list")
        else:
            # get lowest seat numer available, which is unassigned
            seatId = self.availableSeats.removeMin()
            self.seatMapping.insert(userId, seatId)
            # uncomment below line if you want to see the whole assignment after each mapping
            # seatMapping._inorder_traversal(seatMapping.root)
            out_file.write("User " + str(userId) + " reserved seat " + str(seatId))
    
    def cancel(self, userId, seatId):
        # search for userID, as we have userID as key in RBT
        mapping = self.seatMapping.search(userId)

        # if there is no seat mapping for the user
        if mapping.userId == None:
            out_file.write("User " + str(userId)  + " has no reservation to cancel")
        elif mapping.seatId != seatId: # if user mapping exists but not with given seat ID
            out_file.write("User " + str(userId) + " has no reservation for seat " + str(seatId) + " to cancel")
        else:
            # seatMapping._inorder_traversal(seatMapping.root)
            # user has the mapping to given seat
            # delete that mapping from RBT
            self.seatMapping.delete(userId)

            out_file.write("User " + str(userId) + " canceled their reservation\n")

            # insert the vacant seat back into the heap
            self.availableSeats.insert(mapping.seatId)

            # check if there is any user in waiting list
            # if there is, assign the released seat to the 1st user in waiting list
            if self.waitingList.size:
                temp = self.waitingList.removeMax()
                new_user = temp[2]
                new_user_priority = temp[0]
                self.reserve(new_user, new_user_priority)
                # out_file.write("User " + str(new_user) + " reserved seat " + str(mapping.seatId))

            # self.seatMapping._inorder_traversal(self.seatMapping.root)                

if __name__ == "__main__":
    gatorTicketMaster = GatorTicketMaster()
    file_name = sys.argv[1]
    # seatMapping = RedBlackTree()

    if Path(file_name).is_file():
        inp_file = open(file_name,"r+")
        out_file = open(file_name.replace(".txt", "") + "_output_file.txt","w+")

        print("Reading commands from " + f"{file_name}...")

        commands = inp_file.readlines()
        num_commands = len(commands)
        for i in range(0, num_commands):
            if i != 0:
                out_file.write("\n")
            if commands[i][:10] == "Initialize": # completed
                command = commands[i].split('(')
                command = command[1].split(')')
                n = command[0]
                
                gatorTicketMaster.initialize(n)
            elif commands[i][:9] == "Available": # completed
                # print("Total Seats Available : " + str(availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(waitingList.lengthofWaitlist()))
                # out_file.write("Total Seats Available : " + str(availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(waitingList.lengthofWaitlist()))
                gatorTicketMaster.available()
            elif commands[i][:7] == "Reserve": # completed
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId = int(command[0])
                priority = int(command[1].strip())


                # # check if seat is available
                # isSeatAvailable = False
                # if availableSeats.numberOfAvailableSeats():
                #     isSeatAvailable = True
                
                # # if seat is not avilable, then put user in the waitlist
                # # else assign the lowest availablt seat to the user
                # if not isSeatAvailable:
                #     waitingList.insert(userId, priority)
                #     # print(waitingList.line)
                #     out_file.write("User " + str(userId) + " is added to the waiting list")
                # else:
                #     # get lowest seat numer available, which is unassigned
                #     seatId = availableSeats.removeMin()
                #     seatMapping.insert(userId, seatId)
                #     # uncomment below line if you want to see the whole assignment after each mapping
                #     # seatMapping._inorder_traversal(seatMapping.root)
                #     out_file.write("User " + str(userId) + " reserved seat " + str(seatId))
                
                gatorTicketMaster.reserve(userId, priority)
                # out_file.write("Reserving userID: " + userId + " with priority: " + priority)
            elif commands[i][:6] == "Cancel": 
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                seatId = int(command[0])
                userId = int(command[1].strip())

                # # search for userID, as we have userID as key in RBT
                # mapping = seatMapping.search(userId)

                # # if there is no seat mapping for the user
                # if mapping.userId == None:
                #     out_file.write("User " + str(userId)  + " has no reservation to cancel")
                # elif mapping.seatId != seatId: # if user mapping exists but not with given seat ID
                #     out_file.write("User " + str(userId) + " has no reservation for seat " + str(seatId) + " to cancel")
                # else:
                #     # seatMapping._inorder_traversal(seatMapping.root)
                #     # user has the mapping to given seat
                #     # delete that mapping from RBT
                #     seatMapping.delete(userId)

                #     out_file.write("User " + str(userId) + " canceled their reservation")

                #     # insert the vacant seat back into the heap
                #     availableSeats.insert(mapping.seatId)

                #     if waitingList.size:
                #         temp = waitingList.pop(0)
                #         new_user = temp[2]
                #         # new_user_priority = temp[0]

                    
                #     seatMapping._inorder_traversal(seatMapping.root)
                #     # User <userID> canceled their reservation
                
                gatorTicketMaster.cancel(userId, seatId)
                # out_file.write("Cancelling seatId: " + seatId + " with userId: " + userId)
            elif commands[i][:12] == "ExitWaitlist":
                command = commands[i].split('(')
                command = command[1].split(')')
                userId = command[0]
                out_file.write("User: " + seatId + " leaving")
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
                out_file.write("Addig more seats: " + seat_count)
            elif commands[i][:17] == "PrintReservations":
                # current_assignment = [0]*(availableSeats.maxSize - availableSeats.size)
                # print("balle", availableSeats.maxSize - availableSeats.size)
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