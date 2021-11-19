from leaf import Leaf
# TODO implement __str__
class XNode:
    def __init__(self, point):
        self.point = point
        self.parents=[]
        self.left = None
        self.right = None

    def __str__(self):
        return "XNODE" + self.point[0] + "," + self.point[1]

    def attach_right(self, node):
        self.right = node
        self.right.parents.append(self)

    def attach_left(self, node):
        self.left = node
        self.left.parents.append(self)

    def replace_child(self, old, new):

        # Can only replace a leaf
        assert isinstance(old, Leaf)

        # Should be a child
        # TODO remove these debugging statements
        if old not in (self.left, self.right):
            print(old, "is not a child of", self)
            print("children:", (self.left, self.right))

        assert old in (self.left, self.right)
        
        if isinstance(self.left, Leaf) and self.left == old:
            self.attach_left(new)
        elif isinstance(self.right, Leaf) and self.right == old:
            self.attach_right(new)

    def next(self, point):
        """
        Returns the next node in the path to this point's location.
        """
        x, _ = point
        if x < self.point[0]:
            return self.left
        else:
            return self.right

    def is_child_leaf(self, point):
        return self.next(point).is_leaf
