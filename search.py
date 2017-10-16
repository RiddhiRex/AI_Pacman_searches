# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    # Store the starting coordinates of Pacman on the board
    startState = problem.getStartState()
    # Initialize stack for the fringe list
    fringe = util.Stack()
    # Initialize extended list for the nodes that have been visited
    extended = []
    # Push the start state to the stack along with an empty list for the directions for a given path
    fringe.push(([startState], []))
    # Process stack until either it becomes empty or hits goal state
    while not fringe.isEmpty():
        # Pop the current node from the stack
        state, path= fringe.pop()
        # Take the latest coordinate from our path
        current = state[-1]
        # Check if goal state has been reached
        if problem.isGoalState(current) == True:
            return path
        # Check if the current node has been extended
        if current not in extended:
            # Append the node in the extended list
            extended.append(current)
            # Get the successor nodes of the current position - A triplet with (position, direction, cost)
            neighbours = problem.getSuccessors(current)
            for item in neighbours:
                nextState = [item[0]]
                nextPath = [item[1]]
                #Add the successor to the current node (to keep track of our path) and push it to the fringe list
                fringe.push((state + nextState, path + nextPath))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Store the starting coordinates of Pacman on the board
    startState = problem.getStartState()
    # Initialize a queue for the fringe list
    fringe = util.Queue()
    # Initialize extended list for the nodes that have been visited
    extended = []
    # Push the start state to the stack along with an empty list for the directions for a given path
    fringe.push(([startState], []))
    # Process queue until either it becomes empty or hits goal state (seen below)
    while not fringe.isEmpty():
        # Pop the current node from the queue
        state, path = fringe.pop()
        # Take the latest coordinate from our path
        current = state[-1]
        # Check if goal state has been reached
        if problem.isGoalState(current) == True:
            return path
        # Check if the current node has been extended
        if current not in extended:
            # Append the node in the extended list
            extended.append(current)
            # Get the successor nodes of the current position - A triplet with (position, direction, cost)
            neighbours = problem.getSuccessors(current)
            for item in neighbours:
                nextState = [item[0]]
                nextPath = [item[1]]
                # Add the successor to the current node (to keep track of our path) and push it to the fringe list
                fringe.push((state + nextState, path + nextPath))


    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Store the starting coordinates of Pacman on the board
    startState = problem.getStartState()
    # Initialize a priority queue for the fringe list
    fringe = util.PriorityQueue()
    # Initialize extended list for the nodes that have been visited
    extended = []
    # Push the start state to the P-queue along with two empty list(one for the directions, one for cost)
    # with 0 initial priority
    fringe.push(([startState], [], []), 0)
    # Process queue until either it becomes empty or hits goal state
    while not fringe.isEmpty():
        # Pop the current node from the stack
        state, path, cost = fringe.pop()
        # Take the latest coordinate from our path
        current = state[-1]
        # Check if goal state has been reached
        if problem.isGoalState(current) == True:
            return path
        # Check if the current node has been extended
        if current not in extended:
            # Append the node in the extended list
            extended.append(current)
            # Get the successor nodes of the current position - A triplet with (position, direction, cost)
            neighbours = problem.getSuccessors(current)
            for item in neighbours:
                nextState = [item[0]]
                nextPath = [item[1]]
                nextCost = [item[2]]
                totalCost = cost + nextCost
                # Add the successor to the current node (to keep track of our path) and push it to the fringe list
                # Push the path cost up to that node as priority to the queue
                fringe.push((state + nextState, path + nextPath, totalCost), sum(totalCost))




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Store the starting coordinates of Pacman on the board
    startState = problem.getStartState()
    # Initialize a priority queue for the fringe list
    fringe = util.PriorityQueue()
    # Initialize extended list for the nodes that have been visited
    extended = []
    # Push the start state to the stack along with 2 empty lists (action, cost) and the heuristic as priority
    fringe.push(([startState], [], []), heuristic(startState, problem))
    # Process P-queue until either it becomes empty or hits goal state
    while not fringe.isEmpty():
        # Pop the current node from the P-queue
        state, path, cost = fringe.pop()
        # Take the latest coordinate from our path
        current = state[-1]
        # Check if goal state has been reached
        if problem.isGoalState(current) == True:
            return path
        # Check if the current node has been extended
        if current not in extended:
            # Append the node in the extended list
            extended.append(current)
            # Get the successor nodes of the current position - A triplet with (position, direction, cost)
            neighbours = problem.getSuccessors(current)
            for item in neighbours:
                nextState = [item[0]]
                nextPath = [item[1]]
                nextCost = [item[2]]
                totalCost = cost + nextCost
                # Compute the heuristic for the next node
                heu = heuristic(item[0],problem)
                # Push the next node into the queue with path cost + heuristic as priority
                fringe.push((state + nextState, path + nextPath, totalCost), sum(totalCost) + heu)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
