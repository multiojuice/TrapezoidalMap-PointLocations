from leaf import Leaf
import itertools
# TODO implement __str__
class YNode:
    id_iter = itertools.count()

    def __init__(self, segment, id_num):
        self.segment = segment
        self.name = "s" + str(id_num)

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
        return "YNODE " + str(self.segment[0][0]) + "," + str(self.segment[0][1]) + "+" + str(self.segment[1][0]) + "," + str(self.segment[1][1])

    def attach_up(self, node):
        assert node is not None
        node.parents.append(self)
        self.up = node

    def attach_down(self, node):
        assert node is not None
        node.parents.append(self)
        self.down = node

    def replace_child(self, old, new):

        # Can only replace a leaf
        assert isinstance(old, Leaf)

        # Should be a child
        assert old in (self.up, self.down)
        
        if isinstance(self.up, Leaf) and self.up == old:
            self.attach_up(new)
        elif isinstance(self.down, Leaf) and self.down == old:
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

