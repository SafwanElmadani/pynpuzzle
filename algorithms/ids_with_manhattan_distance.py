"""
pynpuzzle - Solve n-puzzle with Python

Iterative deepening depth-first search algorithm

Version : 1.0.0
Author : Hamidreza Mahdavipanah
Repository: http://github.com/mahdavipanah/pynpuzzle
License : MIT License
"""
import heapq
from .util.tree_search import Node


def search(state, goal_state):
    """Iterative deepening A* with manhattan distance heuristic"""
    """Adding f(n)=g(n)+h(n) the heuristic part"""
    def gn(node):
        #return node.gn()
        return node.gn_1()

    tiles_places = []
    for i in range(len(goal_state)):
        for j in range(len(goal_state)):
            heapq.heappush(tiles_places, (goal_state[i][j], (i, j)))

    def hn(node):
        cost = 0
        for i in range(len(node.state)):
            for j in range(len(node.state)):
                if node.state[i][j] == 0:
                    continue
                matched_tile = [x for x in tiles_places if x[0] == node.state[i][j]]
                if matched_tile:
                    tile_i, tile_j = matched_tile[0][1]
                #tile_i, tile_j = tiles_places[node.state[i][j]][1]
                if i != tile_i or j != tile_j:
                    cost += abs(tile_i - i) + abs(tile_j - j)
        return cost

    def fn(node):
        return gn(node) + hn(node)



    """Iterative deepening depth-first"""
    threshold = 0
    queue = []

    threshold = fn(Node(state))

    def dls(node):
        if node.is_goal(goal_state):
            return node
        #if node.depth < depth:
        if fn(node) <= threshold:
            node.expand()
            for child in node.children:
                queue_item = fn(child)
                if queue_item >= threshold:
                    heapq.heappush(queue, queue_item)
                result = dls(child)
                if result:
                    return result
        return None

    answer = None
    while not answer:
        answer = dls(Node(state))
        while True:
            #remove already used threshold
            temp = heapq.heappop(queue)
            if (threshold != temp):
                threshold = temp
                queue.clear()
                break

    output = []
    output.append(answer.state)
    for parent in answer.parents():
        output.append(parent.state)
    output.reverse()

    return output
