import sys
import numpy as np

"""
Construction of Trapezoidal Map
Authors: Daria Chaplin, Owen Sullivan, Collin Tod
"""


def get_traversal(point):
    # TODO
    return ""


def construct_map(ll_bound, ur_bound, line_segments):
    # TODO
    return None


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
    trapezoidal_map = construct_map(ll_bound, ur_bound, line_segments)

    # Accept user-input points and print map traversal
    print("Trapezoidal map built.")
    print("To see a traversal path, enter a point like so: '[x] [y]'")
    print("Enter 'quit' to stop program.")

    while(True):
        user_input = input()
        if user_input == "quit":
            break

        print(get_traversal((coords.split(" ")[0], coords.split(" ")[1])))


if __name__ == "__main__":
    main()
