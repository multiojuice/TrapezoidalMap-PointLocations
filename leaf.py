Point = tuple[float, float]
Segment = tuple[Point, Point]

# TODO implemtn __str__
class Trapezoid:
    def __init__(self, up, down, right, left):
        self.up = up
        self.down = down
        self.right = right
        self.left = left

    def __eq__(self, other):
        return self.up == other.up and \
               self.down == other.down and \
               self.right == other.right and \
               self.left == other.left


class Leaf:

    def __init__(self, trap : Trapezoid):
        self.trap = trap
        self.parents = []

    def __eq__(self, other):
        return isinstance(other, Leaf) and self.trap == other.trap

    def replace_with(self, node):
        """
        Goes through all its parents and replaces itself with the new node,
        then self will end up getting garbage collected
        """
        node.parents = self.parents
        for p in self.parents:
            p.replace_child(self, node)
