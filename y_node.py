from leaf import Leaf
# TODO implement __str__
class YNode:

    def __init__(self, segment):
        self.segment = segment

        # Do calculations needed later for testing if points are above or below
        # this line segment
        (x1, y1), (x2, y2) = self.segment
        dx = x2 - x1
        dy = y2 - y1
        self.slope = dy / dx
        self.y_intercept = y1 - self.slope * x1

        self.up = None
        self.down = None
        self.parents = []

    def __str__(self):
        return "YNODE" + self.segment[0][0] + "," + self.segment[0][1] + "+" + self.point[1][0] + "," + self.point[1][1]

    def attach_up(self, node):
        self.up = node
        self.up.parents.append(self)

    def attach_down(self, node):
        self.down = node
        self.down.parents.append(self)

    def replace_child(self, old, new):

        # Can only replace a leaf
        assert isinstance(old, Leaf)

        # Should be a child
        assert old in (self.up, self.down)
        
        if isinstance(self.up, Leaf) and self.up == self.old:
            self.attach_up(new)
        elif isinstance(self.down, Leaf) and self.down == self.old:
            self.attach_down(new)

    def next(self, point):
        """
        Determines the next node in the path to this point's location
        """
        x, y = point

        # The y value of the line segment at the point's x
        #   y = mx + b
        seg_y_at_x = self.slope * x + self.y_intercept

        if seg_y_at_x < y:
            return self.up
        else:
            return self.down

