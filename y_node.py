class YNode:
    def __init__(self, segment, up, down):
        self.segment = segment

        # Do calculations needed later for testing if points are above or below
        # this line segment
        (x1, y1), (x2, y2) = self.segment
        dx = x2 - x1
        dy = y2 - y1
        self.slope = dy / dx
        self.y_intercept = y1 - slope * x1

        self.up = up
        self.down = down

    def locate(self, point):
        x, y = point

        # The y value of the line segment at the point's x
        #   y = mx + b
        seg_y_at_x = self.slope * x + self.y_intercept

        if seg_y_at_x < y:
            return up.locate(point)
        else:
            return down.locate(point)

