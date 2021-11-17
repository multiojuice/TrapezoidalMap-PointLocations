Point = tuple[float, float]
Segment = tuple[Point, Point]

class Leaf:

    # Adjacent Leaves (Max of 4 in general position) 
    left_top = None
    left_bot = None
    right_top = None
    right_bot = None

    def __init__(self, up, down, right, left):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.parents = []


    def __eq__(self, other):
        return isinstance(other, Leaf)
               self.up == other.up and \
               self.down == other.down and \
               self.right == other.right and \
               self.left == other.left and\


    def next_intersecting(self, seg: Segment):
        """
        Iff seg intersects self, then this finds the next leaf to the right of
        self that the segment also intersects
        """

        assert right_top is not None or right_bot is not None

        # TODO assert that seg actually crosses the right bounds of this trap
        # TODO actually test that this works

        # If their the same (only one right neighbor) no need to see where segment goes
        # (Must end up to the right because there are no intersecting lines in g.p.
        if right_top == right_bot:
            return right_top

        # Line calculations 
        (x1, y1), (x2, y2) = seg
        dy = y2 - y1
        dx = x2 - x1
        slope = dy / dx
        y_intercept = y1 - x1 * slope

        # the x,y of the point that bounds the right hand side of this trap
        right_x, right_y = self.right

        # The y value of seg at the rightmost point of the trapezoid
        y_at_bound = right_x * slope + y_intercept

        if y_at_bound < right_y:
            return self.right_bot
        else:
            return self.right_top


    def swap_on_left(self, leaf: Leaf):
        """
        Replaces the left references to self with leaf
        """
        pass

    def swap_on_right(self, leaf: Leaf):
        """
        Replaces the right references to self with leaf
        """
        pass

    def replace_with(self, node):
        """
        Goes through all its parents and replaces itself with the new node,
        then self will end up getting garbage collected
        """
        node.parents = self.parents
        for p in self.parents:
            p.replace_child(self, node)
