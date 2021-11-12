from leaf import Leaf, Trapezoid # TODO maybe move trapezoid into its own module
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

        # The trapezoid that is a bounding box around the segments
        root_trap = Trapezoid(up=top_wall, down=bot_wall, right=ur_bound, left=ll_bound)

        # Tree starts out as a single rectangular trapezoid
        self.root = Leaf(root_trap)

        for segment in segments:
            self.insert_segment(segment)

    def locate(self, point: Point) -> Leaf:
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

        # Finds the trapezoids where the segment endpoints lie
        trap1, trap2 = map(lambda l: l.trap, (leaf1, leaf2))

        # Check if endpoints end in the same trapezoid or not
        # This is case 2 on the slides
        if leaf1 == leaf2:

            # Construct the 4 new trapezoids that are created by this segment
            top_trap = Trapezoid(up=trap1.up, down=segment, right=p2, left=p1)
            bot_trap = Trapezoid(up=segment, down=trap1.up, right=p2, left=p1)
            right_trap = Trapezoid(up=trap1.up, down=trap1.down, right=trap1.right, left=p2)
            left_trap = Trapezoid(up=trap1.up, down= trap1.down, right=p1, left=trap1.left)

            # Wrap the trapezoids in leaf nodes
            # TODO reassess if this is necessary
            top_leaf = Leaf(top_trap)
            bot_leaf = Leaf(bot_trap)
            right_leaf = Leaf(right_trap)
            left_leaf = Leaf(left_trap)

            sub_root = XNode(p1)
            sub_root.attach_left(left_leaf)

            other_point_node = XNode(p2)

            segment_node = YNode(segment)
            segment_node.attach_up(top_leaf)
            segment_node.attach_down(bot_leaf)

            other_point_node.attach_left(segment_node)
            other_point_node.attach_right(right_leaf)

            sub_root.attach_right(other_point_node)

            if leaf1 == self.root:
                self.root = sub_root
            else:
                leaf1.replace_with(sub_root)

        else:
            pass
            # TODO hard case
