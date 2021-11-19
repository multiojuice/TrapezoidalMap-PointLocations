Authors: Daria Chaplin, Owen Sullivan, Collin Tod

Given an input file formatted as specified in the assignment, run our code as follows:
	python3 trap.py [input.txt]

It will assemble the trapezoidal map and then prompt the user to query points. These queries will display the traversal path to the trapezoid of that point.

Note that our implementation assumes the general position.

We do not handle the degenerative case of two segments forming a triangle rather than a true trapezoid. When we come across a point which shares the same coordinates as one that's already in the map, we increment the new point's x and y values by one to offset it slightly.
