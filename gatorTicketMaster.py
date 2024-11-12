import sys
from pathlib import Path
from RBT import RedBlackTree
from binMinHeap import MinHeap

if __name__ == "__main__":
    file_name = sys.argv[1]
    redBlackTree = None

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
                out_file.write("Initializing " + str(n))
                availableSeats = MinHeap(n)
                # print(availableSeats.storage)
            elif commands[i][:9] == "Available":
                out_file.write("Available")
            elif commands[i][:7] == "Reserve":
                command = commands[i].split('(')
                command = command[1].split(')')
                command = command[0].split(',')
                userId = command[0]
                priority = command[1].strip()
                out_file.write("Reserving userID: " + userId + " with priority: " + priority)
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