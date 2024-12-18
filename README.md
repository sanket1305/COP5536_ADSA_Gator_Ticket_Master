# Gator Ticket Master - README

Gator Logo  
*Welcome to the Gator Ticket Master!*

![Gemini_Generated_Image_6ibrox6ibrox6ibr](https://github.com/user-attachments/assets/3932ee37-270e-40cf-85b4-8397477a01aa)
_Image Generated using Gemini AI_

## **Overview**
Gator Ticket Master is a **priority-based seat reservation system** designed for Gator Events. It ensures efficient management of seat allocation, waitlists, and cancellations using advanced data structures. Whether you're booking a seat or managing event capacity dynamically, this system has you covered.

---

## **Features**
- **Priority-Based Seat Allocation**: Assigns seats based on user priority and timestamp.
- **Dynamic Seat Management**: Add more seats during an event.
- **Waitlist Handling**: Automatically queues users when seats are unavailable.
- **Reservation Updates**: Modify priorities or cancel reservations seamlessly.
- **Custom Data Structures**:
  - Red-Black Tree for reserved seat management.
  - Binary Min-Heap for waitlist and unassigned seat tracking.

---

## **Quick Start**

### **1. Prerequisites**
- Programming Languages: Python.
- Tested Environment: `thunder.cise.ufl.edu` server.

### **2. Installation**
Clone this repository:
```bash
git clone https://github.com/YourUsername/GatorTicketMaster.git
cd GatorTicketMaster
```

### **3. Running the Program**
Choose your language and execute:

#### **Python**
```bash
python3 gatorTicketMaster.py input_file_name
```

### **4. Input/Output Files**
- Input commands are read from `input_file_name`.
- Output is saved to `<input_file_name>_output_file.txt`.

---

## **Supported Commands**

| Command                     | Description                                                                                     |
|-----------------------------|-------------------------------------------------------------------------------------------------|
| `Initialize(seatCount)`     | Set up the event with a specified number of seats.                                             |
| `Available()`               | Display available seats and waitlist length.                                                   |
| `Reserve(userID, priority)` | Reserve a seat or add the user to the waitlist if no seats are available.                       |
| `Cancel(seatID, userID)`    | Cancel a reservation and reassign the seat if applicable.                                      |
| `ExitWaitlist(userID)`      | Remove a user from the waitlist without affecting their reservation status.                     |
| `UpdatePriority(userID, p)` | Update a user's priority in the waitlist while preserving their original timestamp order.       |
| `AddSeats(count)`           | Add new seats to the available pool and assign them to users in the waitlist if applicable.    |
| `PrintReservations()`       | Print all reserved seats along with their assigned user IDs in ascending order of seat IDs.    |
| `ReleaseSeats(id1, id2)`    | Release reservations for users within a specified range of user IDs.                          |
| `Quit()`                    | Terminate the program execution.                                                              |

---

## **Example Usage**

### Input File:
```plaintext
Initialize(5)
Available()
Reserve(1, 1)
Reserve(2, 1)
Cancel(1, 1)
Reserve(3, 1)
PrintReservations()
Quit()
```

### Output File:
```plaintext
5 Seats are made available for reservation
Total Seats Available : 5, Waitlist : 0
User 1 reserved seat 1
User 2 reserved seat 2
User 1 canceled their reservation
User 3 reserved seat 1
[seat 1, user 3]
[seat 2, user 2]
Program Terminated!!
```

---

## **How It Works**

### Data Structures:
1. **Red-Black Tree**:
   - Efficiently manages reserved seats.
   - Stores User ID as the key and Seat ID as associated data.

2. **Binary Min-Heap**:
   - Tracks unassigned seats for quick allocation.

3. **Binary Max-Heap**:
   - Organizes users in the waitlist by priority and timestamp.

### Key Algorithms:
- Assign lowest-numbered available seat first.
- Dynamically reassign canceled seats based on waitlist priority.
- Handle tie-breaking using timestamps (first come, first served).

---

Enjoy managing your Gator events efficiently with Gator Ticket Master! 🐊
