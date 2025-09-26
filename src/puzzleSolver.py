from TileProblem import TileProblem
import copy
import heapq
import random
import argparse
import time
import sys

# Tree Class
class Node:
    def __init__ (self, state, tile_problem, heuristic, g_cost=0, action=""):
        self.state = state
        self.g_cost = g_cost
        if heuristic == 1:
            self.h_cost = tile_problem.heuristic(state, "manhattan") 
        else:
            self.h_cost = tile_problem.heuristic(state, "missing")
        self.parent = None
        self.actions = tile_problem.actions(state)
        self.action = action
        self.f_val = self.f_cost()
    
    def f_cost(self):
        return self.g_cost + self.h_cost

# Helper function to hash states
def state_to_tuple(state):
    """Convert 2D list to hashable tuple"""
    return tuple(tuple(row) for row in state)

# Check if the frontier contains the same node as the child node we are currently observing
def check_frontier(frontier, node):
    for f_cost, tie_breaker, f_node in frontier: 
        if state_to_tuple(node.state) == state_to_tuple(f_node.state): 
            return f_node
    return None 

# Reconstruct path from goal node to root
def reconstruct_path(goal_node):
    path = []
    current = goal_node

    while current.parent:
        if current.action:
            path.insert(0, current.action)
        current = current.parent
    
    return path

# RBFS Method 
def recursive_bfs(root_state, tile_problem, heuristic):
    start_node = Node(root_state, tile_problem, heuristic)
    node_explored = 1
    
    def bfs(tile_problem, node, f_limit, depth=0):
        nonlocal node_explored
        
        node_explored += 1


        if tile_problem.goal_test(node.state):
            path = reconstruct_path(node)
            return (path, f_limit)
        
        # Generate Children (successors)
        successors = []
        for a in node.actions:
            child_state = tile_problem.result(copy.deepcopy(node.state), a)
            child_node = Node(state=child_state, tile_problem=tile_problem, heuristic=heuristic, g_cost = node.g_cost + 1, action=a)
            child_node.parent = node

            # Make sure the f-val is at least the f-val of the parent
            child_node.f_val = max(child_node.f_cost(), node.f_cost())
            successors.append(child_node)

        if not successors:
            return (None, float("inf"))

        # Sort Successors by f-val
        successors.sort(key=lambda x: x.f_val)

        while True:
            best = successors[0]

            if best.f_val > f_limit:
                return (None, best.f_val)
            
            if len(successors) > 1:
                alt = successors[1].f_val
            else:
                alt = float("inf")
            
            # Recursively call to find solution
            res, best.f_val = bfs(tile_problem, best, min(f_limit, alt), depth + 1)

            if res:
                return (res, best.f_val)

            successors.sort(key=lambda x: x.f_val)
        
    
    res, f_limit = bfs(tile_problem, start_node, float("inf"))
    return res

# A* Search Method
def a_star_search(root_state, tile_problem, heuristic):
    moves = []

    # To be Explored nodes ordered by f(n)
    frontier = []
    
    # Explored Nodes
    visited = set()

    start_node = Node(root_state, tile_problem, heuristic)

    heapq.heappush(frontier, (start_node.f_cost(), random.random(), start_node))
    

    while frontier:
        f_cost, _, node = heapq.heappop(frontier)

        if tile_problem.goal_test(node.state):
            moves = reconstruct_path(node)
            return moves

        # Use the state-key to hash
        state_key = state_to_tuple(node.state)
        if state_key in visited:
            continue

        visited.add(state_key)

        for a in node.actions:
            new_state = tile_problem.result(copy.deepcopy(node.state), a)
            new_state_key = state_to_tuple(new_state)
            
            if new_state_key in visited:
                continue

            child_node = Node(new_state, tile_problem, heuristic, node.g_cost + 1, a)
            child_node.parent = node

            existing_node = check_frontier(frontier, child_node)
            if existing_node and existing_node.g_cost <= child_node.g_cost:
                continue
                
            heapq.heappush(frontier, (child_node.f_cost(), random.random(), child_node))
        
    return []

# Helper Functions
def read_puzzle_file(filename):
    puzzle = []

    with open(filename, 'r') as file:
        for line in file:
            row_data = line.strip().split(",")
            row = []
            for r in row_data:
                if r:
                    row.append(int(r))
                else:
                    row.append(None)
            puzzle.append(row)
    return puzzle


def main():              
    
    try:
        # Arg Parsing
        parser = argparse.ArgumentParser(description='Solve sliding tile puzzle using A* search')
        parser.add_argument('algorithm')
        parser.add_argument('n_size')
        parser.add_argument('heuristic')
        parser.add_argument('input_file')
        parser.add_argument('output_file')
        args = parser.parse_args()

        

        curr_state = read_puzzle_file(args.input_file)
        tile_problem = TileProblem(curr_state)
        moves = []

        if args.algorithm == "1":
            moves = a_star_search(curr_state, tile_problem, int(args.heuristic))
        
        if args.algorithm == "2":
            moves = recursive_bfs(curr_state, tile_problem, int(args.heuristic))
        
        res = ','.join(moves)
        with open(args.output_file, 'w') as file:
            file.write(res)


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()