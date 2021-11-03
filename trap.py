import sys
import numpy as np

"""
Construction of Trapezoidal Map
Authors: Daria Chaplin, Owen Sullivan, Collin Tod
"""

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


if __name__ == "__main__":
    main()
