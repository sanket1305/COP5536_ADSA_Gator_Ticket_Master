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
        self.EXT_NODE = Node(userId=None, seatId = None, color='black')
        # root node
        self.root = self.EXT_NODE
    
    # function to perform Left rotation
    def leftRotate(self, x):
        # assume there are 3 nodes...
        # grandparent (x) -> parent (y) -> node
        # when left rotate is called
        # parent (y) will move to top
        # it will have new left pointer to grandparent (x)
        # while doing this old y.left should be transfer to x.right
        # once this is done, update parent pointer mappings
        y = x.right
        x.right = y.left
        if y.left != self.EXT_NODE:
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
    def rightRotate(self, x):
        # assume there are 3 nodes...
        # grandparent (x) -> parent (y) -> node
        # when right rotate is called
        # parent (y) will move to top
        # it will have new right pointer to grandparent (x)
        # while doing this old y.right should be transfer to x.left
        # once this is done, update parent pointer mappings
        y = x.left
        x.left = y.right
        if y.right != self.EXT_NODE:
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

    # function to search a node from ROOT node
    def search(self, userId):
        return self.findNode(self.root, userId)

    # function to find a node from given node
    def findNode(self, node, userId):
        # print(userId, type(userId), node.userId, type(node.userId))
        while node != self.EXT_NODE and userId != node.userId:
            # print("sank")
            if userId < node.userId:
                node = node.left
            else:
                node = node.right
        return node

    # function to handle pointer transfers after deletion
    # is called on nodes with degree 1 or 0
    def swapNodes(self, delNode, childNode):
        # if node 
        if delNode.parent is None:
            self.root = childNode
        elif delNode == delNode.parent.left:
            delNode.parent.left = childNode
        else:
            delNode.parent.right = childNode
        childNode.parent = delNode.parent

    # function to find minimum value in RBT
    # minimum value in RBT will be always in the 
    # lowest node along leftmost path
    def minimum(self, node):
        while node.left != self.EXT_NODE:
            node = node.left
        return node
    
    # function to perform in order traversal on the RBT
    # this function was used for debugging purpose
    # if we feel there is any discrepency after executing any command from the output file
    # we can call inorder traversal after that command execution
    def inorderTraversal(self, node):
        if node is not None:
            self.inorderTraversal(node.left)
            print(node.userId, " ", node.seatId, "...", end=" ")
            self.inorderTraversal(node.right)

    # function to insert a user in RBT 
    def insert(self, userId, seatId):
        # create new node, assign external nodes as left and right childs
        new_node = Node(userId, seatId)
        new_node.left = self.EXT_NODE
        new_node.right = self.EXT_NODE

        # call to insert node method
        self.insertNode(new_node)

    # function to insert newly created node in RBT
    def insertNode(self, node):
        parent = None
        current = self.root

        # check the position where new node should be isnerted
        # at each stage compare if new_node value is 
        # less than or greater than the current node value
        # according to that traverse till the bottom of the tree
        while current != self.EXT_NODE:
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
        self.fixInsert(node)

    # function to fix the discrepancy in RBT by performing required rotations 
    def fixInsert(self, node):
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
                        self.leftRotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.rightRotate(node.parent.parent)
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
                        self.rightRotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.leftRotate(node.parent.parent)
        
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
        node = self.findNode(self.root, userId)

        # check if node found is External Node, then 
        # don't do anything as node does not exists
        if node == self.EXT_NODE:
            return
        
        # if we reached here, it means node found is not external node
        # call delete_node for searched node pointer
        self.deleteNode(node)

    # function to delete the user node from RBT
    def deleteNode(self, node):
        y_original_color = node.color

        # if node's left pointer is external node
        # that mean node has either degree1 or 0
        # replace the node with it's right child 
        # if degree is 0, we will still have external node to replace
        if node.left == self.EXT_NODE:
            # pointer to right node, as we have to call 
            # deleteFix later on this node
            x = node.right

            # replace the node with it's right child
            self.swapNodes(node, node.right)
        elif node.right == self.EXT_NODE: # same as above just for right child
            x = node.left
            self.swapNodes(node, node.left)
        else:
            # if we entered here, that means we have a node with degree 2
            # replace node with the minimum element from it's right subtree
            # remove this minimum element node
            # then call fixDelete method
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.swapNodes(y, y.right)
                y.right = node.right
                y.right.parent = y
            
            # call this function to replace the deleting node
            # with minimum node in it's right subtree
            self.swapNodes(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        # if the deleted node had black color
        # then elting node must have impacted the
        # no. of black nodes in the paths which go through 
        # the subtree strating at deleted node
        # so call delete_fix method, to fix the discrepancies
        if y_original_color == 'black':
            self.fixDelete(x)

    # function to fix any discrepancy in RBT after delete node call
    def fixDelete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.parent.right
                # if x's sibling is red
                # make it black and mark x's parent as red
                # perform left rotation on x's parent
                # change mapping of x's sibling pointer
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.leftRotate(x.parent)
                    sibling = x.parent.right
                
                # if both of x's siblings are black
                # then make sibling color as red
                if sibling.left.color == 'black' and sibling.right.color == 'black':
                    sibling.color = 'red'
                    x = x.parent
                else:
                    # if x's sibling's right child is black 
                    # then make it's left child also black
                    # call right rotation on x's sibling and change sibling mapping
                    if sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rightRotate(sibling)
                        sibling = x.parent.right
                    
                    # make color adjustments for x's sibling and x's parent color
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    sibling.right.color = 'black'
                    # perform left rotate on x's parent
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                # similar to above steps 
                sibling = x.parent.left
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rightRotate(x.parent)
                    sibling = x.parent.left
                if sibling.left.color == 'black' and sibling.right.color == 'black':
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.leftRotate(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    sibling.left.color = 'black'
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = 'black'
