'''
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But -- oh no! -- one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:

.O..

..O.

...O

O...


To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:

.O -> O

..


Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:

O. -> .

.O


Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:

O.O

.O.

O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.


Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The solution will always be less than one billion (10^9).



Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{true, true, false, true, false, true, false, true, true, false}, {true, true, false, false, false, false, true, true, true, false}, {true, true, false, false, false, false, false, false, false, true}, {false, true, false, false, false, false, true, true, false, false}})
Output:
    11567

Input:
Solution.solution({{true, false, true}, {false, true, false}, {true, false, true}})
Output:
    4

Input:
Solution.solution({{true, false, true, false, false, true, true, true}, {true, false, true, false, false, false, true, false}, {true, true, true, false, false, false, true, false}, {true, false, true, false, false, false, true, false}, {true, false, true, false, false, true, true, true}}
Output:
    254

-- Python cases --
Input:
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254
'''

# Instead of generating all (m+1)x(n+1) possible preimages matrices of 0s and 1s and then filtering out those that can lead to the current state
# we optimise the calculation by selecting one by one the columns so that: 
# Given the first column there are certain preimages possible.
# The idea is to store the possible preimages for a given image column in an dictionary 
# and for the next column, we only select the preimages that their first row is the same as the last row of the previous column produced
import numpy as np
from collections import defaultdict
from itertools import product

matrices = np.reshape(list(product([0, 1], repeat=2*2)), (-1, 2, 2)) # all 2x2 matrices
empty = np.array([x for x in matrices if np.sum(x)!=1]).tolist() # all 2x2 matrices that can represent a filled cell
filled = np.array([x for x in matrices if np.sum(x)==1]).tolist() # all 2x2 matrices that can represent an empty cell

possible_states = {1: (filled), 0: (empty)}


def overlaped_preimages(col1, col2):   
    for pre_col1 in col1:
        for pre_col2 in col2:
            if pre_col1[-1] == pre_col2[0]:
                yield tuple(pre_col1)+(pre_col2[1],)
          
        
def preimages_of_column(cur):
    preimages = possible_states[cur[0]]
    for i, cell in filter(lambda c: c[0]!=0, enumerate(cur)):  
        preimages = overlaped_preimages(preimages, possible_states[cell])
    return tuple([tuple(zip(*pre)) for pre in preimages])    
 

def solution(cur):
    cur=tuple(zip(*cur))
    preimages = defaultdict(int) 
    for p in preimages_of_column(cur[0]):
        preimages[p[1]] += 1  
        
    for i, col in filter(lambda c: c[0]!=0, enumerate(cur)):
        next_preimages = dict()
        for p in preimages_of_column(col):
            if p[0] in preimages:
                if p[1] in next_preimages:
                    next_preimages[p[1]] = preimages[p[0]] + next_preimages[p[1]]
                else:
                    next_preimages[p[1]] = preimages[p[0]]
        
      
        preimages = next_preimages

    return sum(preimages.values())

