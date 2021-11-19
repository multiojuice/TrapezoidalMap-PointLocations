import sys
from trap_map import TrapMap
from leaf import Leaf
from x_node import XNode
from y_node import YNode

"""
Construction of Trapezoidal Map
Authors: Daria Chaplin, Owen Sullivan, Collin Tod
"""


def generateMatrix(root):
    dic = {}



def traverseTree(root, dic):
    if type(root) is Leaf:
        print("thing")












def main():
    fp = open(sys.argv[1])
    line_segments = []
    ll_bound, ur_bound = None, None

    # Read input file (bounding box coords and line segments)
    for idx, line in enumerate(fp):
        coords = [float(x) for x in line.split(" ")]
        if idx == 1:
            ll_bound = (coords[0], coords[1])
            ur_bound = (coords[2], coords[3])
        elif idx > 1:
            line_segments.append((
                (coords[0], coords[1]),
                (coords[2], coords[3])))

    # Build trapezoidal map with randomized incremental algorithm
    # FIXME: line_segments shouldn't only be the first element, remove slice once hard case is implemented
    trap_map = TrapMap(line_segments[:1], ll_bound, ur_bound)

    # Accept user-input points and print map traversal
    print("Trapezoidal map built.")
    print("To see a traversal path, enter a point like so: '[x] [y]'")
    print("Enter 'quit' to stop program.")

    while(True):
        user_input = input()
        if user_input == "quit":
            break

        # split then cast the user's input
        x, y = map(int, user_input.split(" "))

        print(trap_map.path_to((x, y)))


if __name__ == "__main__":
    main()
