class Node:
    # constructor
    # left right child, parent pointer
    # default color of node has to be red, as new node inserted into tree will be red
    def __init__(self, userId, seatId, color='red'):
        self.userId = userId
        self.seatId = seatId
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

# Red-Black Tree (RBT) implementation
class RedBlackTree:
    # constructor
    def __init__(self):
        # external node
        self.NIL = Node(userId=None, seatId = None, color='black')
        # root node
        self.root = self.NIL
    
    # function to insert a user in RBT 
    def insert(self, userId, seatId):
        # create new node, assign external nodes as left and right childs
        new_node = Node(userId, seatId)
        new_node.left = self.NIL
        new_node.right = self.NIL

        # call to insert node method
        self._insert_node(new_node)

    # function to insert newly created node in RBT
    def _insert_node(self, node):
        parent = None
        current = self.root

        # check the position where new node should be isnerted
        # at each stage compare if new_node value is 
        # less than or greater than the current node value
        # according to that traverse till the bottom of the tree
        while current != self.NIL:
            parent = current
            if node.userId < current.userId:
                current = current.left
            else:
                current = current.right
        
        # as we have found the place where new node is to be inserted
        # set new_nodes parent pointer
        node.parent = parent

        # if tree is empty, mark the new_node as root
        # else we have the parent, assign new_node to it's left or right 
        # based on new node value
        if parent is None:
            self.root = node
        elif node.userId < parent.userId:
            parent.left = node
        else:
            parent.right = node
        
        # new node inserted in RBT, always has red color
        node.color = 'red'

        # as new node is inserted, now we need insert_fix
        # to fix any discrepancies which might have introduced
        # so call insert_fix on current node (as it's new one in RBT)
        self._fix_insert(node)

    # function to fix the discrepancy in RBT by performing required rotations 
    def _fix_insert(self, node):
        # keep working on it until there are 2 consecutive red nodes
        while node != self.root and node.parent.color == 'red':
            # if parent is grandparent's left child, then 
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                # if uncle color is red
                # what all we have so far?
                # curr_node, parent are red, uncle is red
                # we can mark parent and uncle as black and grandparent as red
                # will this create any issue? why not?
                # No, because even though we are changing color of grandparent black => red
                # we are adding black color in child path, by making parent and uncle as red => black
                # so total number of black node in this path will remain same
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    # as we marked the grandparent as re, there is possibility that grandparent = red and grandparent.parent = red
                    # so shift, new_node pointer to grandparent and repeat fixing
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    # as uncle is black, 
                    # if new_node is parent's right child then perform LR rotation
                    # or if new_node is parent's left child then perform just R rotation
                    # and change the colors
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.right_rotate(node.parent.parent)
                    # after this rotation
            else:
                # new_node parent is right child of new_node's grandparent
                uncle = node.parent.parent.left
                # same as above, if uncle is red
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    # as uncle is black, 
                    # if new_node is parent's left child then perform LR rotation
                    # or if new_node is parent's right child then perform just R rotation
                    # and change the colors
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.left_rotate(node.parent.parent)
        
        # after performing all oprations
        # there is possibility that we might have marked root as red
        # so make it black
        # will this create any issue? No... why not?
        # making root as Red => Black, will not affect
        # no. of black node counts for other nodes in the RBT
        self.root.color = 'black'

    # function to delete the user from RBT
    def delete(self, userId):
        # before caling delete_node check if node exists in RBT
        node = self._find_node(self.root, userId)

        # check if node found is External Node, then 
        # don't do anything as node does not exists
        if node == self.NIL:
            return
        
        # if we reached here, it means node found is not external node
        # call delete_node for searched node pointer
        self._delete_node(node)

    # function to delete the user node from RBT
    def _delete_node(self, node):
        y_original_color = node.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        # if the deleted node had black color
        # then elting node must have impacted the
        # no. of black nodes in the paths which go through 
        # the subtree strating at deleted node
        # so call delete_fix method, to fix the discrepancies
        if y_original_color == 'black':
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == 'black' and sibling.right.color == 'black':
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.right_rotate(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    sibling.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    sibling = x.parent.left
                if sibling.left.color == 'black' and sibling.right.color == 'black':
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.left_rotate(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    sibling.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # function to perform right rotation
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # function to search a node
    def search(self, userId):
        return self._find_node(self.root, userId)

    # function to find a node 
    def _find_node(self, node, userId):
        # print(userId, type(userId), node.userId, type(node.userId))
        while node != self.NIL and userId != node.userId:
            # print("sank")
            if userId < node.userId:
                node = node.left
            else:
                node = node.right
        return node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # function to find minimum value in RBT
    # minimum value in RBT will be always in the 
    # lowest node along leftmost path
    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    # function to perform in order traversal on the RBT
    # this function was used for debugging purpose
    # if we feel there is any discrepency after executing any command from the output file
    # we can call inorder traversal after that command execution
    def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.userId, " ", node.seatId, "...", end=" ")
            self._inorder_traversal(node.right)