Point = tuple[float, float]
Segment = tuple[Point, Point]

class Leaf:
    def __init__(self, up, down, right, left):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.parents = []
        # Adjacent Leaves (Max of 4 in general position)
        self.left_top = None
        self.left_bot = None
        self.right_top = None
        self.right_bot = None


    def __eq__(self, other):
        return isinstance(other, Leaf) and \
               self.up == other.up and \
               self.down == other.down and \
               self.right == other.right and \
               self.left == other.left and\
               self.left_top == other.left_top and \
               self.left_bot == other.left_bot and \
               self.right_top == other.right_top and \
               self.right_bot == other.right_bot


    def __str__(self):
        return "Trap" + self.left[0] + "," + self.left[1] + "+" + self.right[0] + "," + self.right[1]

    def next_intersecting(self, seg: Segment):
        """
        Iff seg intersects self, then this finds the next leaf to the right of
        self that the segment also intersects
        """

        assert self.right_top is not None or self.right_bot is not None

        # TODO assert that seg actually crosses the right bounds of this trap
        # TODO actually test that this works

        # If their the same (only one right neighbor) no need to see where segment goes
        # (Must end up to the right because there are no intersecting lines in g.p.
        if self.right_top == self.right_bot:
            return self.right_top

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
        if self.left_top.right_top == self:
            self.left_top.right_top = leaf

        if self.left_top.right_bot == self:
            self.left_top.right_bot = leaf

        if self.left_bot.right_top == self:
            self.left_bot.right_top = leaf

        if self.left_bot.right_bot == self:
            self.left_bot.right_bot = leaf

    def swap_on_right(self, leaf: Leaf):
        """
        Replaces the right references to self with leaf
        """
        if self.right_top.left_top == self:
            self.right_top.left_top = leaf

        if self.right_top.left_bot == self:
            self.right_top.left_bot = leaf

        if self.right_bot.left_top == self:
            self.right_bot.left_top = leaf

        if self.right_bot.left_bot == self:
            self.right_bot.left_bot = leaf

    def replace_with(self, node):
        """
        Goes through all its parents and replaces itself with the new node,
        then self will end up getting garbage collected
        """
        node.parents = self.parents
        for p in self.parents:
            p.replace_child(self, node)
