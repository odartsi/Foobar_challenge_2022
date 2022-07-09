'''
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

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
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
    '''
from fractions import *
import numpy as np

# transforming the matrix into a matrix that represents the probabilities
def transform_to_prob(m):
    sum_list = list(map(sum, m))
    bool_indices = list(map(lambda x: x == 0, sum_list))
    indices = set([i for i, x in enumerate(bool_indices) if x])
    new_m = []
    for i in range(len(m)):
        new_m.append(list(map(lambda x: Fraction(0, 1) if(sum_list[i] == 0) else Fraction(x,sum_list[i]), m[i]))) 
    # make sure that all the terminal states are at the end of the matrix
    # if certain rows have to change their location, change the same columns location as well
    # if we exchange row 1 with row 2 then column 1 has to change with column 2 to represent correctly the probability
    transform_m = []
    zeros_m = []
    for i in range(len(new_m)):
        if i not in indices:
            transform_m.append(new_m[i])
        else:
            zeros_m.append(new_m[i])
    transform_m.extend(zeros_m)

    tm = []
    for i in range(len(transform_m)):
        tm.append([])
        extend_m = []
        for j in range(len(transform_m)):
            if j not in indices:
                tm[i].append(transform_m[i][j])
            else:
                extend_m.append(transform_m[i][j])
        tm[i].extend(extend_m)
    return [tm, len(zeros_m)]

def transition_matrix(m,lr):
    l = len(m) - lr
    q = []
    r = []
    for i in range(l):
        q.append([int(i==j)-m[i][j] for j in range(l)])
        r.append(m[i][l:])
    return [q, r]
   

def get_denominator(array): 
    lcm = np.lcm.reduce([fr.denominator for fr in array])
    vals = [int(fr.numerator * lcm / fr.denominator) for fr in array]
    vals.append(lcm)
    return vals

def multiply_matrix(a, b):
    m = []
    # dimesion of final matrix
    rows = len(a)
    cols = len(b[0])
    iters = len(a[0])

    for i in range(rows):
        m_row = []
        for j in range(cols):
            sum = 0
            for it in range(iters):
                sum += a[i][it] * b[it][j]
            m_row.append(sum)
        m.append(m_row)
    return m

def copy_matrix(m):
    cm = []
    for i in range(len(m)):
        cm.append([])
        for j in range(len(m[i])):
            cm[i].append(Fraction(m[i][j].numerator, m[i][j].denominator))
    return cm

def gaussian_elimination(m, values):
    mat = copy_matrix(m)
    for i in range(len(mat)):
        index = -1
        for j in range(i, len(mat)):
            if mat[j][i].numerator != 0:
                index = j
                break
        mat[i], mat[index] = mat[index], mat[j]
        values[i], values[index] = values[index], values[i]
        for j in range(i+1, len(mat)):
            if mat[j][i].numerator == 0:
                continue
            ratio = -mat[j][i]/mat[i][i]
            for k in range(i, len(mat)):
                mat[j][k] += ratio * mat[i][k]
            values[j] += ratio * values[i]
    res = [0 for i in range(len(mat))]
    for i in range(len(mat)):
        index = len(mat) -1 -i
        end = len(mat) - 1
        while end > index:
            values[index] -= mat[index][end] * res[end]
            end -= 1
        res[index] = values[index]/mat[index][index]
    return res

def transpose_matrix(m):
    tm = []
    for i in range(len(m)):
        for j in range(len(m)):
            if i == 0:
                tm.append([])
            tm[j].append(m[i][j])
    return tm

def inverse_matrix(m):
    tm = transpose_matrix(m)
    m_inv = []
    for i in range(len(tm)):
        values = [Fraction(int(i==j), 1) for j in range(len(m))]
        m_inv.append(gaussian_elimination(tm, values))
    return m_inv

def solution(m):
    # when there are only 0s it is 100% prob that will terminate
    if not np.any(m):
        return [1,1]
    p = transform_to_prob(m)
    q,r = transition_matrix(*p)
    inv = inverse_matrix(q)
    m = multiply_matrix(inv,r)
    array = get_denominator(m[0]) 
    return array

#solution([[0, 1, 0, 0, 0, 1],[4, 1, 0, 3, 2, 0],
#        [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 1, 0, 3, 2, 0]])
#solution([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
