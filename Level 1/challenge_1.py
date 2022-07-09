'''
Write a function called solution(data, n) that takes in a list of less than 100 integers and a number n, 
and returns that same list but with all of the numbers that occur more than n times removed entirely. 
The returned list should retain the same ordering as the original list - you don't want to mix up those 
carefully-planned shift rotations! For instance, if data was [5, 10, 15, 10, 7] and n was 1, solution(data, n) 
would return the list [5, 15, 7] because 10 occurs twice, and thus was removed from the list entirely.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([1, 2, 3], 0)
Output:
    

Input:
solution.solution([1, 2, 2, 3, 3, 3, 4, 5, 5], 1)
Output:
    1,4
'''

def solution(data, n): 
    from collections import Counter
    counting_set= Counter(data)
    x=[key for key,value in counting_set.items() if value>n]
    data=list(filter(lambda i : i not in x, data)) 
    return data
