import math

from leaf import Leaf
import itertools

class XNode:
    id_iter = itertools.count()
    def __init__(self, point, isP = True):
        self.point = point
        self.parents = []
        self.left = None
        self.right = None

        if isP:
            self.name = "p" + str(math.floor((next(XNode.id_iter) + 1) / 2))
        else:
            self.name = "q" + str(math.floor((next(XNode.id_iter) + 1) / 2))

    def __str__(self):
        return "XNODE " + str(self.point[0]) + "," + str(self.point[1])

    def attach_right(self, node):
        assert node is not None
        node.parents.append(self)
        self.right = node

    def attach_left(self, node):
        assert node is not None
        node.parents.append(self)
        self.left = node

    def replace_child(self, old, new):

        # Can only replace a leaf
        assert isinstance(old, Leaf)

        # Should be a child
        # TODO remove these debugging statements
        if old not in (self.left, self.right):
            print(old, "is not a child of", self)
            print("children:", (str(self.left), str(self.right)))

        assert old in (self.left, self.right)
        
        if isinstance(self.left, Leaf) and self.left == old:
            self.attach_left(new)
        elif isinstance(self.right, Leaf) and self.right == old:
            self.attach_right(new)

    def next(self, point):
        """
        Returns the next node in the path to this point's location.
        """

        if self.right is None:
            print(self, "right is none")
        assert self.right is not None
        assert self.left is not None

        x, _ = point
        if x < self.point[0]:
            return self.left
        else:
            return self.right

    def is_child_leaf(self, point):
        return self.next(point).is_leaf
