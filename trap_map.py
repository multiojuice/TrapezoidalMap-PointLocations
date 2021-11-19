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

            # TODO there HAS to be a neater way of doing this
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

            # The leftmost trapezoid of the single endpoint split
            # Has all the same bounds as leaf_begin except a new right point
            leaf_leftmost = Leaf(up=leaf_begin.up, down=leaf_begin.down,
                                 left=leaf_begin.left, right=p1)

            # The top of the single endpoint split. May be merged with new
            # leaves on the right
            merge_top = Leaf(up=leaf_begin.up, down=segment,
                             left=p1, right = None)

            # The bottom of the single endpoint split. May be merged with new
            # leaves on the right
            merge_bot = Leaf(up=segment, down=leaf_begin.down,
                             left=p1, right = None)

            # Set up neighbors for these new leaves
            leaf_leftmost.left_top = leaf_begin.left_top
            leaf_leftmost.left_bot = leaf_begin.left_bot
            leaf_leftmost.right_top = merge_top
            leaf_leftmost.right_bot = merge_bot

            # Swap out old leaf's references to itself with new leftmost
            leaf_begin.swap_on_left(leaf_leftmost)

            # Mark the merge leaves as having the leftmost leaf to their left
            merge_top.left_top = leaf_begin
            merge_top.left_bot = leaf_begin
            merge_bot.left_top = leaf_begin
            merge_bot.left_bot = leaf_begin

            # TODO set up the tree structure for these new splits (note that
            # begin_top and begin_bot may be merged with a trapezoid to the
            # right

            # We want the first leaf to be processed (if there is one) to be
            # the next intersecting leaf to the right of the beginning leaf
            prev_leaf = leaf_begin
            cur_leaf = leaf_begin.next_intersecting(segment) 

            while True:

                assert prev_leaf.right_top == cur_leaf or prev_leaf.right_bot == cur_leaf

                # Whether we cut the section above the segment or not
                cut_top = False

                if prev_leaf.right_top != prev_leaf.right_bot:

                    # If there are two right neigbors of the previous leaf,
                    # then the segment should be on the bottom for the bounding
                    # point to cut the top
                    cut_top = prev_leaf.right_bot == cur_leaf

                else:
                    assert cur_leaf.left_bot == prev_leaf or cur_leaf.left_top == prev_leaf

                    # If there are two left neighbors of the current leaf, the
                    # segment should come from the bottom one in order to cut
                    # the top section
                    cut_top = cur_leaf.left_bot == prev_leaf


                # Should we cut off the top section or the bottom section
                # during this split?
                if cut_top:

                    # Mark the end of the top merge
                    merge_top.right = cur_leaf.left

                    # Save the old top to link later
                    old_merge_top = merge_top

                    # New top
                    merge_top = Leaf(up=cur_leaf.up, down=segment,
                                     left=cur_leaf.left, right=None)

                    # TODO link up old_merge_top etc.
                else:

                    # Mark the end of the bottom merge
                    merge_bot.right = cur_leaf.left

                    # Save the old bottom that we cut off to link it later
                    old_merge_bot = merge_bot

                    # New bottom 
                    merge_bot = Leaf(up=segment, down=cur_leaf.down,
                                     left=cur_leaf.left, right=None)

                    # TODO link up old_merge_bot etc.


                # Now that we've merged/cut, jump out if we are at the end
                if cur_leaf is leaf_end:
                    break


                # Constructs and inserts the new subgraph
                seg_split = YNode(segment)
                seg_split.attach_up(merge_top)
                seg_split.attach_down(merge_bot)
                cur_leaf.replace_with(seg_split)

            leaf_rightmost = Leaf(up=leaf_end.up, down=leaf_end.down,
                                  left=p2, right=leaf_end.right)

            # Link up leaf rightmost with everything
            leaf_end.swap_right(leaf_rightmost)
            leaf_rightmost.right_top = leaf_end.right_top
            leaf_rightmost.right_bot = leaf_end.right_bot
            leaf_rightmost.left_top = merge_top
            leaf_rightmost.left_bot = merge_bot
            

            # Cut off the two potentially merging leaves with right endpoint of
            # segment
            merge_top.right = p2
            merge_bot.right = p2

            # Link the merging leaves to rightmost
            merge_top.right_top = leaf_rightmost
            merge_top.right_bot = leaf_rightmost
            merge_bot.right_top = leaf_rightmost
            merge_bot.right_bot = leaf_rightmost

            # TODO construct the subgraph and expand it at leaf_end in the tree
