class RBNode:
    # constructor
    # left right child, parent pointer
    # default color of node has to be red, as new node inserted into tree will be red
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None
    
    # function to get gradparent of node
    def grandparent(self):
        # if node does not have parent, then it won't have grand parent as well.
        # e.g. root
        if self.parent is None:
            return None
        return self.parent.parent
    
    # function to get sibling of node
    def sibling(self):
        # if node does not have parent, it does not have sibling
        if self.parent is None:
            return None
        
        # check if current node is left child, return child child as sibling and vice versa
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # function to get the uncle of node
    def uncle(self):
        #  if there is no parent, there won't be any uncle as well
        if self.parent is None:
            return None
        
        # we have sibling() function use it to get parent's sibling (uncle)
        return self.parent.sibling()
    
# function to implement Red Black Tree
class RedBlackTree:
    # constructor
    def __init___(self):
        self.root = None
    
    # function to search a value in RB Tree
    def search(self, value):
        # start search from root node
        curr_node = self.root

        # keep trversing until we reach bottom of tree (via any branch)
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        
        # return None, as we reached end of tree and value is not found
        return None
    
    # function to insert a node in RB Tree, similar to BST insertion
    def insert(self, value):
        # Regular insertion
        new_node = RBNode(value)

        # if tree is empty, mark the new_node as root
        if self.root is None:
            self.root = new_node
        else:
            # start from root node
            curr_node = self.root

            while True:
                # if new value is less than curr_node value, 
                # then traverse to left subtree
                # else traverse to right subtree
                if value < curr_node.value:
                    # if left child is None, then make new_node as left_child
                    # update, the pointers and break as we have inserted the node
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        
        # as the new node has been inserted, 
        # call fixing step (rotations), to maintain RBT properties
        self.insert_fix(new_node)
    
    # function to fix RB tree properties after insertion
    def insert_fix(self, new_node):
        # keep working on it until there are 2 consecutive red nodes
        while new_node.parent and new_node.parent.color == 'red':
            # if parent is grandparent's left child, then 
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                # if uncle color is red
                # what all we have so far?
                # curr_node, parent are red, uncle is red
                # we can mark parent and uncle as black and grandparent as red
                # will this create any issue? why not?
                # No, because even though we are changing color of grandparent black => red
                # we are adding black color in child path, by making parent and uncle as red => black
                # so total number of black node in this path will remain same
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    # as we marked the grandparent as re, there is possibility that grandparent = red and grandparent.parent = red
                    # so shift, new_node pointer to grandparent and repeat fixing
                    new_node = new_node.grandparent()
                else:
                    # as uncle is black, perform LR rotation and change the colors
                    # before rotation it would look like (6 is newly inserted node)
                    #            / (it's black beacuse child is red, and initially the tree was stable)
                    #           7
                    #         // \
                    #        5    10
                    #       / \\    
                    #      2    6
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    # after left rotation it would look like
                    #            /
                    #           7
                    #         // \
                    #        6    10
                    #      //
                    #     5
                    #    /
                    #   2
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    # after color change (note, new_node was changed before left rotation)
                    #            //
                    #           7
                    #          / \
                    #         6   10
                    #       //
                    #      5
                    #     /
                    #    2
                    self.rotate_right(new_node.grandparent())
                    # after right roatate
                    #            /
                    #           6
                    #         // \\
                    #        5    7
                    #       /      \
                    #      2        10
                    # analysis on number of block nodes in path
                    # before node addition both 7 -> 2 and 7 -> 10 has 2 black nodes.. (7, 2) and (7, 10) respectively
                    # after node addition both 7 -> 2 and 7 -> 10 has 2 black nodes.. (6, 2) and (6, 10) respectively
                    # properties maintained.
            else:
                # new_node parent is right child of new_node's grandparent
                uncle = new_node.uncle()
                # same as above, if uncle is red
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    # do RL rotation or just Right roation
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'
    
    # function for left rotation of RB Tree
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        # if the above assignment is NOT None,
        # then it means we have to update parent pointer for that node as well.
        if right_child.left is not None:
            right_child.left.parent = node
        
        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        
        right_child.left = node
        node.parent = parent
    
    # function for right rotation of RB Tree
    left_child = node.left
    node.left = left_child.right

    # if the above assignment is NOT None,
    # then it means we have to update parent pointer for that node as well.
    if left_child.right is not None:
        left_child.right.parent = node
    
    left_child.parent = node.parent

    if node.parent is None:
        self.root = left_child
    elif node == node.parent.right:
        node.parent.right = left_child
    else:
        node.parent.left = left_child
    
    left_child.right = node
    node.parent = left_child