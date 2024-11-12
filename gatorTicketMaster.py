# scenarios remaining: if for a person, prioeity is updated, should we update its timestamp as well?

import sys
from pathlib import Path
from RBT import RedBlackTree
from binMinHeap import MinHeap
from binMaxHeap import MaxHeap

if __name__ == "__main__":
    file_name = sys.argv[1]
    seatMapping = RedBlackTree()

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
                n = int(command[0])
                out_file.write(str(n) + " Seats are made available for reservation")

                # created 1-n seats
                availableSeats = MinHeap(n)

                # initialize waiting list, which is empty at the start
                waitingList = MaxHeap()

                # print(availableSeats.storage)
            elif commands[i][:9] == "Available":
                print("Total Seats Available : " + str(availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(waitingList.lengthofWaitlist()))
                out_file.write("Total Seats Available : " + str(availableSeats.numberOfAvailableSeats()) + ", Waitlist : " + str(waitingList.lengthofWaitlist()))
            elif commands[i][:7] == "Reserve":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId = int(command[0])
                priority = int(command[1].strip())

                # check if seat is avaiable
                isSeatAvailable = False
                if availableSeats.numberOfAvailableSeats():
                    isSeatAvailable = True
                
                # if seat is not avilable, then put user in the waitlist
                # else assign the lowest availablt seat to the user
                if not isSeatAvailable:
                    print("sorry, can't do the reservation")
                else:
                    # get lowest seat numer available, which is unassigned
                    seatId = availableSeats.removeMin()
                    seatMapping.insert(userId, seatId)
                    # uncomment below line if you want to see the whole assignment after each mapping
                    # seatMapping._inorder_traversal(seatMapping.root)
                    out_file.write("User " + str(userId) + " reserved seat " + str(seatId))
                # out_file.write("Reserving userID: " + userId + " with priority: " + priority)
            elif commands[i][:6] == "Cancel":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                seatId = command[0]
                userId = command[1].strip()
                out_file.write("Cancelling seatID: " + seatId + " with userId: " + userId)
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
                out_file.write("Printing reservations...")
            elif commands[i][:12] == "ReleaseSeats":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId1 = command[0]
                userId2 = command[1].strip()
                out_file.write("Releasing seats in range: " + userId1 + " : " + userId2)
            elif commands[i][:4] == "Quit":
                out_file.write("Terminating the program")
            else:
                out_file.write("Invalid command")
        print()
    else:
        print(f"{file_name} does not exist")