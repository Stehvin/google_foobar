# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 20:07:18 2017

@author: Stehvin
"""

'''
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and broken the bunnies out
of Lambda's prison - and now you need to escape from the space station 
as quickly and as orderly as possible! The bunnies have all gathered 
in various locations throughout the station, and need to make their way
towards the seemingly endless amount of escape pods positioned in other
parts of the station. You need to get the numerous bunnies through the 
various rooms to the escape pods. Unfortunately, the corridors between 
the rooms can only fit so many bunnies at a time. What's more, many of 
the corridors were resized to accommodate the LAMBCHOP, so they vary 
in how many bunnies can move through them at a time. 

Given the starting room numbers of the groups of bunnies, the room 
numbers of the escape pods, and how many bunnies can fit through at a 
time in each direction of every corridor in between, figure out how 
many bunnies can safely make it to the escape pods at a time at peak.

Write a function answer(entrances, exits, path) that takes an array of 
integers denoting where the groups of gathered bunnies are, an array 
of integers denoting where the escape pods are located, and an array 
of an array of integers of the corridors, returning the total number 
of bunnies that can get through at each time step as an int. The 
entrances and exits are disjoint and thus will never overlap. The path 
element path[A][B] = C describes that the corridor going from A to B 
can fit C bunnies at each time step.  There are at most 50 rooms 
connected by the corridors and at most 2000000 bunnies that will fit 
at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 
at each time step.  (Note that in this example, room 3 could have sent 
any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the 
final answer remains the same.)

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int list) entrances = [0]
    (int list) exits = [3]
    (int) path = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], 
    [9, 0, 0, 0]]
Output:
    (int) 6

Inputs:
    (int list) entrances = [0, 1]
    (int list) exits = [4, 5]
    (int) path = [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], 
    [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]]
Output:
    (int) 16

Use verify [file] to test your solution and see how it does. When you 
are finished editing your code, use submit [file] to submit your 
answer. If your solution passes the test cases, it will be removed 
from your home folder.
'''

def answer(entrances, exits, path):
    
    # set constants
    n = len(path) + 2   # number of nodes (including source and sink)
    MAX_CAP = 2000001   # max capacity of edge
    
    # add source and sink to adjacency matrix
    weightArray = [[0] * n]
    for p in path:
        p2 = [0] + p + [0]
        weightArray += [p2]
    weightArray += [[0] * n]
    
    # allow source->entrance and exit->sink edges to have max capacity
    for entry in entrances:
        weightArray[0][entry + 1] = MAX_CAP
    for exit in exits:
        weightArray[exit + 1][-1] = MAX_CAP
    
    # find a route using depth-first search
    def findRoute(weightArray, source, sink):
        stack = [source]
        routes = {source:[]}
        while(stack):
            start = stack.pop()
            for index, capacity in enumerate(weightArray[start]):
                if capacity > 0 and index not in routes:
                    routes[index] = routes[start] + [(start, index)]
                    
                    # once a route is found, return the route and its min capacity
                    if index == sink:
                        minCap = MAX_CAP
                        for edge in routes[index]:
                            minCap = min(minCap, weightArray[edge[0]][edge[1]])
                        return routes[index], minCap
                    stack.append(index)
        return None, None
    
    # Ford-Fulkerson Algorithm
    # iterate over paths, updating weightArray each iteration,
    # until no possible paths remain
    def fordFulkAlg(weightArray, source, sink):
        maxFlow = 0
        route, minCap = findRoute(weightArray, source, sink)
        while route != None:
            maxFlow += minCap
            for edge in route:
                weightArray[edge[0]][edge[1]] -= minCap
                weightArray[edge[1]][edge[0]] += minCap
            route, minCap = findRoute(weightArray, source, sink)
        return maxFlow
    
    return fordFulkAlg(weightArray, 0, n - 1)