import sys
import numpy as np
from trap_map import TrapMap
from x_node import XNode
from y_node import YNode
import pprint

"""
Construction of Trapezoidal Map
Authors: Daria Chaplin, Owen Sullivan, Collin Tod
"""

# x_number_counter = 0
# y_number_counter = 0
# t_number_counter = 0
#
#

def ido(name, q_off, s_off, t_off, trap_name_map):

    if name[0] == 't':
        name = trap_name_map[name]

    plain = int(name[1:])

    if name[0] == 'q':
        plain += q_off
    if name[0] == 's':
        plain += s_off
    if name[0] == 't':
        plain += t_off
    return plain - 1


def generateMatrix(root):
    dic = {}
    traverse_tree(root, dic)
    p_map = {}
    q_map = {}
    s_map = {}
    t_map = {}

    for key in dic.keys():
        if key[0] == 'p':
            p_map[key] = True
        elif key[0] == 'q':
            q_map[key] = True
        elif key[0] == 's':
            s_map[key] = True

        for val in dic[key]:
            if val[0] == 'p':
                p_map[val] = True
            elif val[0] == 'q':
                q_map[val] = True
            elif val[0] == 's':
                s_map[val] = True
            elif val[0] == 't':
                t_map[val] = True

    l_traps = list(t_map.keys())
    parsed_traps = list((map(lambda x: int(x[1:]), l_traps)))
    parsed_traps.sort()
    sorted_traps = list(map(lambda y: "t" + str(y), parsed_traps));

    trap_name_map = {}

    for i in range(0, len(sorted_traps)):
        trap_name_map[sorted_traps[i]] = "t" + str(i)

    q_off = len(p_map)
    s_off = q_off + len(q_map)
    t_off = s_off + len(s_map)
    total_size = t_off + len(t_map);

    matrix = []

    for i in range(total_size):
        matrix.append([0] * total_size)

    for key in dic.keys():
        for val in dic[key]:
            first = ido(key, q_off, s_off, t_off, trap_name_map)
            second = ido(val, q_off, s_off, t_off, trap_name_map)

            matrix[second][first] = 1

    matrix.insert(0, [0])

    for i in range(total_size):
        num = i
        letter = 'p'
        if i >= t_off:
            num -= t_off
            letter = 't'
        elif i >= s_off:
            num -= s_off
            letter = 's'
        elif i >= q_off:
            num -= q_off
            letter = 'q'

        matrix[0].append(letter + str(num + 1))
        matrix[i + 1].insert(0, letter + str(num + 1))

    for row in matrix:
        print(row)

    return trap_name_map


def traverse_tree(root, dic):
    if type(root) is XNode:
        if root.name not in dic:
            dic[root.name] = [root.left.name, root.right.name]
        else:
            dic[root.name].append(root.left.name)
            dic[root.name].append(root.right.name)

        traverse_tree(root.right, dic)
        traverse_tree(root.left, dic)
    elif type(root) is YNode:
        if root.name not in dic:
            dic[root.name] = [root.up.name, root.down.name]
        else:
            dic[root.name].append(root.up.name)
            dic[root.name].append(root.down.name)

        traverse_tree(root.up, dic)
        traverse_tree(root.down, dic)

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
    trap_map = TrapMap(line_segments, ll_bound, ur_bound)
    generateMatrix(trap_map.root)


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
