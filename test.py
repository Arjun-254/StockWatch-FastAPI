class RBNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.parent = None
        self.red = False
        self.val = val


class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.parent = None
        self.nil.left = None
        self.nil.right = None
        self.nil.red = False
        self.root = self.nil

    def insert(self, val):
        new_node = RBNode(val)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        parent = None
        current = self.root

        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                return
            
        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

       
        
        self.fix_insert(new_node)

    def fix_insert(self, new_node):
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left  # uncle

                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)

                    new_node.parent.red = False
                    new_node.parent.parent.red = True

                    self.rotate_left(new_node.parent.parent)
            else:
                u = new_node.parent.parent.right  # uncle

                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    
                    new_node.parent.red = False
                    new_node.parent.parent.red = True

                    self.rotate_right(new_node.parent.parent)
            
        
        self.root.red = False

    def rotate_left(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.nil:
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

    def rotate_right(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.right = x
        x.parent = y

    def __repr__(self):
        lines = []
        self.print_tree(self.root, lines)
        return '\n'.join(lines)

    def print_tree(self, node, lines, level=0):
        if node.val != 0:
            self.print_tree(node.left, lines, level + 1)

            lines.append('-' * 4 * level + '> ' +
                         str(node.val) + ' ' + ('r' if node.red else 'b'))

            self.print_tree(node.right, lines, level + 1)

    def search(self, node, key):
            if node == self.nil or key == node.val:
                return node

            if key < node.val:
                return self.search(node.left, key)
            return self.search(node.right, key)

    def delete_node(self, key):
        z = self.search(self.root, key)
        if z == self.nil:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.nil:  
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red
        
        if y_original_color == False:
            self.delete_fix(x)

    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fix(self, x):
        while x != self.root and x.red == False:
            if x == x.parent.left:
                w = x.parent.right  #Sibling
                if w.red:         #case 2  make sibling black, parent red and rotate_left(parent)
                    w.red = False
                    x.parent.red = True
                    self.rotate_left(x.parent)
                    w = x.parent.right

                if w.left.red == False and w.right.red == False:  
                    if w.parent.red:        #case 4 make parent black, make sibling red x = self.root (terminator case)
                        w.parent.red = False
                        w.red = True
                        x = self.root
                    else:
                        w.red = True   #case 3 (make sibling red and shift double black up)
                        x = x.parent    # shift double black upar
                else:
                    if w.right.red == False:  #case 5 left child of sibling is red
                        w.left.red = False   # make left child black, sibling red and rotate right sibling
                        w.red = True
                        self.rotate_right(w)
                        w = x.parent.right

                    w.red = x.parent.red  #Case 6 make siblings color = parents color
                    x.parent.red = False  #make parent black
                    w.right.red = False   #make right child of sibling black
                    self.rotate_left(x.parent)
                    x = self.root   #terminator case
            else:
                w = x.parent.left
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self.rotate_right(x.parent)
                    w = x.parent.left
                if w.right.red == False and w.left.red == False:
                    if w.parent.red:       #case 4
                        w.parent.red = False
                        w.red = True
                        x = self.root
                    else:
                        w.red = True   #case 3
                        x = x.parent    #shift double black upar
                else:
                    if w.left.red == False:
                        w.right.red = False
                        w.red = True
                        self.rotate_left(w)
                        w = x.parent.left

                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    self.rotate_right(x.parent)
                    x = self.root
        x.red = False

    

    

tree = RBTree()


tree.insert(10)
tree.insert(18)
tree.insert(7)
tree.insert(15)
tree.insert(16)
tree.insert(30)
tree.insert(25)
tree.insert(40)
tree.insert(60)
tree.insert(2)
tree.insert(1)
tree.insert(70)
print(tree)
tree.delete_node(3)
print("\nAfter deleting 3 Tree is \n")
print(tree)
