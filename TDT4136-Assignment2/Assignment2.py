# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:43:04 2022

@author: Kristian
"""
from typing import TypeVar
import heapq
from test1 import Map_Obj 
import csv
from warnings import warn



class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end):
    

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),) #Allows diagonal movement 

    # Loop until you find the end
    while len(open_list) > 0:

        
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #set the current position as blocked for future use
        maze[current_node.position[0]][current_node.position[1]] = -1
        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            within_range_criteria = [
                node_position[0] > (len(maze) - 1),
                node_position[0] < 0,
                node_position[1] > (len(maze[len(maze) - 1]) - 1),
                node_position[1] < 0,
            ]
            
            if any(within_range_criteria):
                continue

            # Make sure walkable terrain
            if int(maze[node_position[0]][node_position[1]]) == -1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + int(maze[child.position[0]][child.position[1]])*20 #weighs the value of the traversed cell with the sum range multiplied dimensionally 2*(1+2+3+4)=20
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) #heuristic
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)


x = input("Task: ")
themap = Map_Obj(task=int(x))

#Return a list of list matrix of the csv file
with open(themap.path_to_map, 'r') as read_obj:
    samf = list(csv.reader(read_obj))

rute = astar(samf, (themap.start_pos[0], themap.start_pos[1]) , (themap.goal_pos[0], themap.goal_pos[1]))

#Shows map without path
print(rute)
themap.show_map(None)

#Shows map with path and start plus end
for i in range(len(rute)-2):    
    themap.set_cell_value([rute[i+1][0], rute[i+1][1]], 5)
themap.show_map(None)

