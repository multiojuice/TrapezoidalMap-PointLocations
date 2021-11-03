class XNode:
    
    def __init__(self, point,left, right):
        self.point = point
        self.left = left
        self.right = right

    def locate(self, point):
        x, _ = point
        if x < self.point[0]:
            return left.locate(point)
        else:
            return right.locate(point)
