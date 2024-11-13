import time
import sys

# Red-Black Tree Node
class RedBlackTreeNode:
    def __init__(self, userID, seatID):
        self.userID = userID
        self.seatID = seatID
        self.color = 'R'  # 'R' for Red, 'B' for Black
        self.left = None
        self.right = None
        self.parent = None

# Red-Black Tree Class
class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackTreeNode(0, 0)  # sentinel node
        self.TNULL.color = 'B'
        self.root = self.TNULL #  # Root of the tree, initialized to sentinel

    def left_rotate(self, x):
        # Left rotation to maintain tree balance
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        # Right rotation to maintain tree balance
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fixup(self, k):
        # Fixes Red-Black Tree properties after insertion
        while k.parent.color == 'R':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right # Uncle Node 
                if u.color == 'R': # Case 1
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.right: # Case 2 
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left # Uncle Node
                if u.color == 'R':
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'B'

    def insert(self, userID, seatID):
        # Inserts a new node into the Red-Black Tree
        node = RedBlackTreeNode(userID, seatID)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'R'

        # Locate the position to insert the new node
        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.userID < x.userID:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None: # Insert as root node
            self.root = node
        elif node.userID < y.userID:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 'B'
            return

        if node.parent.parent == None:
            return

        self.insert_fixup(node)

    def search(self, userID):
        # Searches the tree for a node by UserID
        node = self.root
        while node != self.TNULL:
            if userID == node.userID:
                return node
            elif userID < node.userID:
                node = node.left
            else:
                node = node.right
        return None

    def delete(self, node):
        pass

# Binary Min-Heap for Waitlist and Available Seats
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        # Adds an item to the heap and restores heap properties
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Removes and returns the minimum item from the heap
        if not self.heap:
            return None
        min_item = self.heap[0]
        last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = last_item
            self._sift_down(0)
        return min_item

    def peek(self):
        return self.heap[0] if self.heap else None

    def size(self):
        return len(self.heap)

    def _sift_up(self, index):
        # Maintains heap order property on insertion
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _sift_down(self, index):
        # Maintains heap order property on removal
        min_index = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        size = len(self.heap)

        if left_child < size and self.heap[left_child] < self.heap[min_index]:
            min_index = left_child
        if right_child < size and self.heap[right_child] < self.heap[min_index]:
            min_index = right_child

        if min_index != index:
            self.heap[index], self.heap[min_index] = self.heap[min_index], self.heap[index]
            self._sift_down(min_index)


# Max-Heap based on priority and timestamp for waitlist
class PriorityHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Removes and returns the maximum priority item from the heap
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        max_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return max_item

    def peek(self):
        return self.heap[0] if self.heap else None

    def size(self):
        return len(self.heap)

    def _sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self._compare(self.heap[index], self.heap[parent]) > 0:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
        max_index = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self._compare(self.heap[left], self.heap[max_index]) > 0:
            max_index = left
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[max_index]) > 0:
            max_index = right
        if index != max_index:
            self.heap[index], self.heap[max_index] = self.heap[max_index], self.heap[index]
            self._sift_down(max_index)

    def _compare(self, a, b):
        # Compare based on priority first, then timestamp
        if a[0] != b[0]:
            return a[0] - b[0]
        return b[1] - a[1]  # Earlier timestamp wins if priorities are equal


# Gator Ticket Master Class
class GatorTicketMaster:
    def __init__(self):
        self.red_black_tree = RedBlackTree()
        self.available_seats = MinHeap()
        self.waitlist = PriorityHeap()
        self.reservations = {}
        self.waitlist_counter = 0
        self.seat_count = 0

    def Initialize(self, seatCount):
        # Initializes seat count and adds seats to available seats heap
        try:
            seatCount = int(seatCount)
            if seatCount <= 0:
                raise ValueError
            self.seat_count = seatCount
            for seat in range(1, seatCount + 1):
                self.available_seats.push(seat)
            print(f"{seatCount} Seats are made available for reservation")
        except ValueError:
            print("Invalid input. Please provide a valid number of seats.")

    def Available(self):
        # Displays total seats available and waitlist size
        print(f"Total Seats Available : {self.available_seats.size()}, Waitlist : {self.waitlist.size()}")

    def Reserve(self, userID, userPriority):
        # Reserves a seat for a user or adds them to the waitlist if seats are full
        userID = int(userID)
        userPriority = int(userPriority)
        if self.available_seats.size() > 0:
            seatID = self.available_seats.pop()
            self.red_black_tree.insert(userID, seatID)
            self.reservations[userID] = seatID
            print(f"User {userID} reserved seat {seatID}")
        else:
            self.waitlist.push((userPriority, self.waitlist_counter, userID))
            self.waitlist_counter += 1
            print(f"User {userID} is added to the waiting list")


    def Cancel(self, seatID, userID):
        seatID = int(seatID)
        userID = int(userID)
        # Check if the user has an active reservation for the specified seat
        if userID in self.reservations and self.reservations[userID] == seatID:
            del self.reservations[userID]
            node_to_remove = self.red_black_tree.search(userID)
            if node_to_remove:
                self.red_black_tree.delete(node_to_remove)
            print(f"User {userID} canceled their reservation")
            
            # If the waitlist is not empty, reassign the seat to the highest-priority user
            if self.waitlist.size() > 0:
                userPriority, timestamp, next_userID = self.waitlist.pop()
                self.reservations[next_userID] = seatID
                self.red_black_tree.insert(next_userID, seatID)
                print(f"User {next_userID} reserved seat {seatID}")
            else:
                # Return the seat to the available seats heap if the waitlist is empty
                self.available_seats.push(seatID)
        else:
            # Print message if the user has no reservation for the specified seat
            print(f"User {userID} has no reservation for seat {seatID} to cancel")



    def ExitWaitlist(self, userID):
        userID = int(userID)
        # Find and remove the user from the waitlist
        for index, (priority, timestamp, user) in enumerate(self.waitlist.heap):
            if user == userID:
                # Remove the user by index and reheapify
                self.waitlist.heap.pop(index)
                if index < self.waitlist.size():  # Reheapify if items remain
                    self.waitlist._sift_down(index)
                    self.waitlist._sift_up(index)
                print(f"User {userID} is removed from the waiting list")
                return
        print(f"User {userID} is not in waitlist")

    def UpdatePriority(self, userID, userPriority):
        userID = int(userID)
        userPriority = int(userPriority)
        for index, (priority, timestamp, user) in enumerate(self.waitlist.heap):
            if user == userID:
                # Update priority and reheapify
                self.waitlist.heap[index] = (userPriority, timestamp, userID)
                self.waitlist._sift_down(index)
                self.waitlist._sift_up(index)
                print(f"User {userID} priority has been updated to {userPriority}")
                return
        print(f"User {userID} priority is not updated")

    def AddSeats(self, count):
        try:
            count = int(count)
            if count <= 0:
                raise ValueError
            # Add each new seat to the available seats heap
            for seat in range(self.seat_count + 1, self.seat_count + count + 1):
                self.available_seats.push(seat)
            self.seat_count += count
            print(f"Additional {count} Seats are made available for reservation")

            # Assign seats to users on the waitlist if there are available seats
            assigned_users = []
            while self.available_seats.size() > 0 and self.waitlist.size() > 0:
                seatID = self.available_seats.pop()
                userPriority, timestamp, userID = self.waitlist.pop()
                self.reservations[userID] = seatID
                self.red_black_tree.insert(userID, seatID)
                assigned_users.append((userID, seatID))

            # Print assigned reservations
            for userID, seatID in assigned_users:
                print(f"User {userID} reserved seat {seatID}")

        except ValueError:
            print("Invalid input. Please provide a valid number of seats.")

    def inorder_traversal(self, node, reservations):
        if node != self.red_black_tree.TNULL:
            self.inorder_traversal(node.left, reservations)
            if node.userID in self.reservations:
                seatID = self.reservations[node.userID]
                reservations[seatID] = node.userID
            self.inorder_traversal(node.right, reservations)


    def PrintReservations(self):

        reservations = {}
        self.inorder_traversal(self.red_black_tree.root, reservations)
        # Sort reservations based on seat number
        for seatID in sorted(reservations.keys()):
            userID = reservations[seatID]
            print(f"Seat {seatID}, User {userID}")

    
    def ReleaseSeats(self, userID1, userID2):
        userID1 = int(userID1)
        userID2 = int(userID2)

        # Ensure the range is valid
        if userID2 < userID1:
            print("Invalid input. Please provide a valid range of users.")
            return

        print(f"Reservations of the Users in the range [{userID1}, {userID2}] are released")
        released_seats = []
        users_to_remove = []

         # Release reservations within the specified range
        for userID in range(userID1, userID2 + 1):
            if userID in self.reservations:
                seatID = self.reservations[userID]
                released_seats.append(seatID)
                del self.reservations[userID]
                node_to_remove = self.red_black_tree.search(userID)
                if node_to_remove:
                    self.red_black_tree.delete(node_to_remove)
            else:
                users_to_remove.append(userID)

        # Rebuild the waitlist without the users in the range
        new_waitlist = PriorityHeap()  # Change this to PriorityHeap
        for priority, timestamp, user in self.waitlist.heap:
            if user not in users_to_remove:
                new_waitlist.push((priority, timestamp, user))
        self.waitlist = new_waitlist

        # Return released seats to available and assign if waitlist is populated
        for seatID in released_seats:
            self.available_seats.push(seatID)

        assigned_users = []
        while self.available_seats.size() > 0 and self.waitlist.size() > 0:
            seatID = self.available_seats.pop()
            priority, timestamp, userID = self.waitlist.pop()
            self.reservations[userID] = seatID
            self.red_black_tree.insert(userID, seatID)
            assigned_users.append((userID, seatID))

        for userID, seatID in assigned_users:
            print(f"User {userID} reserved seat {seatID}")


    def Quit(self):
        print("Program Terminated!!")
        sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gatorTicketMaster.py <input_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = input_filename.split('.')[0] + "_output_file.txt"

    gtm = GatorTicketMaster()

    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        sys.stdout = output_file  # Redirect stdout to the output file

        for line in input_file:
            command = line.strip().split('(')
            function_name = command[0]
            args = command[1].rstrip(')').split(',') if len(command) > 1 else []

            if function_name == 'Initialize':
                gtm.Initialize(args[0])
            elif function_name == 'Available':
                gtm.Available()
            elif function_name == 'Reserve':
                gtm.Reserve(args[0], args[1])
            elif function_name == 'Cancel':
                gtm.Cancel(args[0], args[1])
            elif function_name == 'ExitWaitlist':
                gtm.ExitWaitlist(args[0])
            elif function_name == 'UpdatePriority':
                gtm.UpdatePriority(args[0], args[1])
            elif function_name == 'AddSeats':
                gtm.AddSeats(args[0])
            elif function_name == 'PrintReservations':
                gtm.PrintReservations()
            elif function_name == 'ReleaseSeats':
                gtm.ReleaseSeats(args[0], args[1])
            elif function_name == 'Quit':
                gtm.Quit()

        sys.stdout = sys.__stdout__  # Reset stdout to the console

    print(f"Output has been written to {output_filename}")

if __name__ == "__main__":
    main()
