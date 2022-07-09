'''
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. **You also know that if a beam hits a corner, it will bounce back in exactly the same direction.** And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and **returns an integer of the number of distinct directions** that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).

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
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
    '''
import math

def distance_of_two_points(p1,p2):
    return math.sqrt(pow(p2,2) + pow(p1,2))
    
def get_mirror_coordinates(dimensions,position,my_pos,grid_size):
    
    [x,y] = dimensions
    (px,py) = position
    
    # get double the distance of the left,right,top and bottom wall in order to
    # define the next positions
    x_right = (x-px)*2
    x_left = px*2
    x = [px-my_pos[0]]*(grid_size*2+1)
    
    y_up = (y-py)*2 
    y_down = py*2
    y = [py-my_pos[1]]*(grid_size*2+1)
    
    for i in range(grid_size+1,grid_size*2+1):
        x[i] = x[i-1]+x_right if (i-grid_size-1)%2==0 else x[i-1]+x_left
    for i in range(grid_size-1,-1,-1):
        x[i] = x[i+1]-x_left if (grid_size-1-i)%2==0 else x[i+1]-x_right
    
    for i in range(grid_size+1,grid_size*2+1):
        y[i] = y[i-1]+y_up if (i-grid_size-1)%2==0  else y[i-1]+y_down
    for i in range(grid_size-1,-1,-1):
        y[i] = y[i+1]-y_down if (grid_size-1-i)%2==0 else y[i+1]-y_up
    return x,y

def solution(dimensions, my_position, trainer_position, distance):
    grid_size = (distance//min(dimensions))+1 
    my_x, my_y = get_mirror_coordinates(dimensions,my_position,my_position,grid_size)
    trainer_x, trainer_y = get_mirror_coordinates(dimensions,trainer_position,my_position,grid_size)
 

    angle_dist = {}
    for x in my_x:
        for y in my_y:
            if (x==0 and y==0):
                continue
            d = distance_of_two_points(y,x)
            if d<=distance:
                # use the arc tangent to identify the same 'beams'and keep 
                # the one with smallest distance 
                beam =  math.atan2(y, x)
                if beam in angle_dist:
                    if d<angle_dist[beam]:
                        angle_dist[beam] = d
                else:
                    angle_dist[beam] = d
    
    possible_points=set()
    for x in trainer_x:
        for y in trainer_y:
            d = distance_of_two_points(y,x)
            if d<=distance:
                beam =  math.atan2(y, x)
                if beam in angle_dist:
                    if d<angle_dist[beam]:
                        angle_dist[beam] = d
                        possible_points.add(beam)
                else:
                    angle_dist[beam] = d
                    possible_points.add(beam)
    
    return len(possible_points)
