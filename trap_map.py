from leaf import Leaf
from x_node import XNode
from y_node import YNode

Point = tuple[float, float]
Segment = tuple[Point, Point]

class TrapMap:

    def __init__(self, segments: list[Segment], ll_bound: Point, ur_bound: Point):
        """
        Constructs a TrapMap using the segments in `segments`. 
        """

        self.segments = segments

        minx, miny = ll_bound
        maxx, maxy = ur_bound

        # Top and bottom segments of the bounding box
        top_wall = (minx, maxy), ur_bound
        bot_wall = ll_bound, (maxx, miny)

        # Tree starts out as a single rectangular trapezoid
        self.root = Leaf(up=top_wall, down=bot_wall, right=ur_bound, left=ll_bound)

        for segment in segments:
            self.insert_segment(segment)

    def locate(self, point: Point) -> Leaf:
        """
        Returns the leaf that represents the trapezoidal area that `point`
        would lie in
        """
        assert self.root is not None

        node = self.root

        # Traverse the tree until the correct leaf node is found
        while not isinstance(node, Leaf):
            node = node.next(point)

        assert isinstance(node, Leaf)
        return node

    def path_to(self, point):
        """
        Returns a list of the nodes on the path to `point`
        """

        path = []

        # assume that there is something in the map
        assert self.root is not None
        node = self.root

        # Traverse the tree until the correct leaf node is found
        while not isinstance(node, Leaf):
            path.append(node)
            node = node.next(point)

        return path

    def insert_segment(self, segment: Segment):

        assert self.root is not None

        p1, p2 = segment

        # Finds the location of the segment endpoints
        leaf1, leaf2 = map(self.locate, segment)

        assert isinstance(leaf1, Leaf)
        assert isinstance(leaf2, Leaf)

        # Check if endpoints end in the same trapezoid or not
        # This is case 2 on the slides
        if leaf1 == leaf2:

            # Construct the 4 new trapezoids that are created by this segment
            top_leaf = Leaf(up=leaf1.up, down=segment, right=p2, left=p1)
            bot_leaf = Leaf(up=segment, down=leaf1.up, right=p2, left=p1)
            right_leaf = Leaf(up=leaf1.up, down=leaf1.down, right=leaf1.right, left=p2)
            left_leaf = Leaf(up=leaf1.up, down= leaf1.down, right=p1, left=leaf1.left)

            # Set neighbors of the left leaf
            left_leaf.left_top = leaf1.left_top
            left_leaf.left_bot = leaf1.left_bot
            left_leaf.right_top = top_leaf
            left_leaf.right_bot = bot_leaf

            # Set neighbors of the right leaf
            right_leaf.left_top = top_leaf
            right_leaf.left_bot = bot_leaf
            right_leaf.right_top = leaf1.right_top
            right_leaf.right_bot = leaf1.right_bot

            # Set neighbors of the top leaf
            top_leaf.right_top = right_leaf
            top_leaf.right_bot = right_leaf
            top_leaf.left_top = left_leaf
            top_leaf.left_bot = left_leaf

            # Set neighbors of the bot leaf
            bot_leaf.right_top = right_leaf
            bot_leaf.right_bot = right_leaf
            bot_leaf.left_top = left_leaf
            bot_leaf.left_bot = left_leaf

            # Constructs the new subtree that this leaf turns into
            sub_root = XNode(p1)
            sub_root.attach_left(left_leaf)

            other_point_node = XNode(p2)

            segment_node = YNode(segment)
            segment_node.attach_up(top_leaf)
            segment_node.attach_down(bot_leaf)

            other_point_node.attach_left(segment_node)
            other_point_node.attach_right(right_leaf)

            sub_root.attach_right(other_point_node)

            # If the leaf is root, it doesn't have any parents and thus the
            # root reference itself should be swapped
            if leaf1 == self.root:
                self.root = sub_root
            else:
                leaf1.replace_with(sub_root)

        else:

            # TODO maybe rename like this everywhere?
            leaf_begin = leaf1
            leaf_end = leaf2

            # TODO split up leaf_begin

            # The leftmost trapezoid of the single endpoint split
            # Has all the same bounds as leaf_begin except a new right point
            leaf_leftmost = Leaf(up=leaf_begin.up, down=leaf_begin.down,
                                 left=leaf_begin.left, right=p1)

            # The top of the single endpoint split
            leaf_begin_top = Leaf(up=leaf_begin.up, down=segment,
                                  left=p1, right = leaf_begin.right)

            # The bottom of the single endpoint split
            leaf_begin_bot = Leaf(up=segment, down=leaf_begin.down,
                                  left=p1, right = leaf_begin.right)

            # Set up neighbors for these new leaves
            leaf_leftmost.left_top = leaf_begin.left_top
            leaf_leftmost.left_bot = leaf_begin.left_bot
            leaf_leftmost.right_top = leaf_begin_top
            leaf_leftmost.right_bot = leaf_begin_bot

            # TODO set up the tree structure for these new splits (note that
            # begin_top and begin_bot may be merged with a trapezoid to the
            # right

            # TODO iterate over every leaf that seg intersects, splitting them horizontally
                # TODO figure out if the segment is coming on top of or below the left bounding point. 
                #      this is important because the new segment will block the
                #      bounding point on the opposite side, meaning that it
                #      will be merged with the previous bot/top left leaf to
                #      this one.
            # TODO split up leaf_end

