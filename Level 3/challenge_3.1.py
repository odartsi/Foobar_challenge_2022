'''
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two distinct processes: 
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs. The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, and the device might survive. Too many, and you might overload the mass capacitors and create a singularity at the heart of the space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!) 

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP. Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string) that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done! M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would need to pass, so the solution would be "1". 
However, if M = "2" and F = "4", it would not be possible.

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
Solution.solution('2', '1')
Output:
    1

Input:
Solution.solution('4', '7')
Output:
    4

-- Python cases --
Input:
solution.solution('4', '7')
Output:
    4

Input:
solution.solution('2', '1')
Output:
    1
'''

def solution(m,f):
    m=int(m)
    f=int(f)
    k=max(m,f)
    l=min(m,f)
    generation=0
    
    
    # if the one of the two is equal to 1 the other number 
    # always indicates the generation
    if min(m,f) ==1: 
        return str(max(m,f)-1)
        
    # it is never possible to have a pair of even numbers
    if m==f or (m%2==f%2==0):
        return "impossible"
    
    # when the two numbers are large or they have a big difference
    # it takes a long time to reach down to 1, for that the max number is
    # devided by minimun number and the output indicates how many generations
    # have to pass to reach a pair where the original minumum number will not 
    # appear ( for example (1378236581, 120000) will take 1378236581//120000=11485
    # generations to reach a number different than 12000. And once I have this
    # generation I can calculate the m out of it and the f will be the 12000. 
    if abs(len(str(m))-len(str(f))) >3:
        generation = k//l 
        m=k-generation*l
        f=l
        
    # Main part -> trying to go back to a value m or/and f ==1   
    while min(f,m)>1:
        k=max(m,f)
        l=min(m,f)
        m=k-l
        f=l
        generation +=1
        if m==f or (m%2==f%2==0) or min(m,f)==0:
            return "impossible"
        
        
    return str(generation+max(m,f)-1)