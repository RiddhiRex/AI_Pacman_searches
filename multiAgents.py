# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # Generate successors of the current game state
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() # Successor game state positions
        newFood = successorGameState.getFood() # Successor food positions
        newGhostStates = successorGameState.getGhostStates() #successor ghost positions
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        if successorGameState.isWin():
            return float("inf") # Return infinity if goal is reached
        foodPositions = newFood.asList() # Coordinates of all food positions
        foodDist = []
        # Calculate distance to each food and find minimum
        for fPosition in foodPositions:
            dist = util.manhattanDistance(fPosition, newPos)
            if dist != 0:
                foodDist.append(dist)
        if len(foodDist) == 0:
            minFoodDist = 0
        else:
            minFoodDist = min(foodDist)
        # Current ghost distance
        ghostDist = util.manhattanDistance(newPos, currentGameState.getGhostPosition(1))
        # Assign a score based on game score and ghost distance
        totalScore = ghostDist + successorGameState.getScore()
        # Calculate amount of food remaining
        foodRemaining = len(foodPositions)
        # Reduce the score by a factor of the distance to the minimum food
        totalScore = totalScore - 5 * minFoodDist
        # Increase score if the current position is on a food dot
        if newPos in currentGameState.getCapsules():
            totalScore += 100
        # Increase score if only one food dot is left
        if foodRemaining == 1:
            totalScore += 1000
        # Increase score if successor state's food > current state's food
        if foodRemaining < len(currentGameState.getFood().asList()):
            totalScore += 100
        # Decrease score if the Pacman stops
        if action == Directions.STOP:
            totalScore -= 5

        return totalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        score, action = self.maxFunction(gameState, self.depth)
        return action

    def maxFunction(self, gameState, depth):
        """
        maxFunction recursively computes the max value for each successor state.
        The traversal is done from the root till the leaves in the depth first search manner
        and the values are returned all the way to the top. This function will be executed by MAX nodes
        where the MAX nodes chooses the highest value among the options.
        This is done until the terminal states are reached where the function is the utility value.
        """
        # Return there is no move to make if the game is over
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "noMove"

        # Get all  possible legal actions
        legalAction = gameState.getLegalActions()
        val = []
        for action in legalAction:
            # For each legal action, call the minFunction of minimax
            val.append(self.minFunction(gameState.generateSuccessor(self.index, action), depth, 1))
        # Assign alpha with maximum value among its children
        alpha = max(val)
        # To find the index of the maximum value alpha
        for i in range(len(val)):
            if val[i] == alpha: \
                    alphaIdx = i
        bestIndex = alphaIdx
        return alpha, legalAction[bestIndex]

    def minFunction(self, gameState, depth, agent):
        """
        minFunction recursively computes the min value for each successor state.
        The traversal is done from the root till the leaves in the depth first search manner
        and the values are returned all the way to the top. This function will be executed by each MIN agent
        and the least value among the options is chosen each time.
        This is done until the terminal states are reached where the function is the utility value.
        :param gameState:
        :param depth:
        :param agent:
        :return:
        """
        # Return there is no move to make if the game is over
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "noMove"

        # To find the number of min agents in the game
        ghostCount = gameState.getNumAgents() - 1
        # To find the number of legal actions
        legalAction = gameState.getLegalActions(agent)
        val = []
        # Determining if next is max move or min move
        if agent != ghostCount:
            for action in legalAction:
                val.append(self.minFunction(gameState.generateSuccessor(agent, action), depth, agent + 1))
        else:
            for action in legalAction:
                val.append(self.maxFunction(gameState.generateSuccessor(agent, action), (depth - 1)))
        # Assign beta with minimum value of its children
        beta = min(val)
        # To find the index of the minimum value child
        for i in range(len(val)):
            if (val[i] == beta): \
                    betaIdx = i
        leastIndex = betaIdx
        return beta, legalAction[leastIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose():
                return gameState.getScore()

            # Initially assign the score as -infinity
            score = -float("inf")
            # Get the legal actions
            legal_actions = gameState.getLegalActions()
            # Initialise an optimal action in the start of the move
            optimal_action = Directions.STOP

            for action in legal_actions:
                v = minValue(gameState.generateSuccessor(0, action), depth, alpha, beta, 1)
                # Assign least value returned by minValue function as v and compare with the previous score
                if v > score:
                    score = v
                    optimal_action = action
                alpha = max(alpha, score)
                if score > beta:
                    return score
            if depth > 0:
                return score
            else:
                return optimal_action

        def minValue(gameState, depth, alpha, beta, ghostCount):
            if gameState.isLose() or gameState.isWin():
                return gameState.getScore()

            score = float("inf")
            legalActions = gameState.getLegalActions(ghostCount)
            newGhostCount = ghostCount + 1
            if ghostCount == (gameState.getNumAgents() - 1):
                newGhostCount = 0

            for action in legalActions:
                if newGhostCount == 0:
                    if depth == self.depth - 1:
                        v = self.evaluationFunction(gameState.generateSuccessor(ghostCount, action))
                    else:
                        v = maxValue(gameState.generateSuccessor(ghostCount, action), depth + 1, alpha, beta)
                else:
                    v = minValue(gameState.generateSuccessor(ghostCount, action), depth, alpha, beta, newGhostCount)
                if v < score:
                    score = v
                beta = min(beta, score)
                if score < alpha:
                    return score
            return score

        return maxValue(gameState, 0, -float("inf"), float("inf"))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        The MAX nodes work exactly the same way as Minimax and 
        Chance nodes are introduced in Expectimax where the average
        of values of all its children is taken as the chance node value. 
        """
        score, action = self.maxFunction(gameState, self.depth)
        return action

    def maxFunction(self, gameState, depth):
        """
        maxFunction recursively computes the max value for each successor state.
        The traversal is done from the root till the leaves in the depth first search manner
        and the values are returned all the way to the top. This function will be executed by MAX nodes
        where the MAX nodes chooses the highest value among the options.
        This is done until the terminal states are reached where the function is the utility value.
        """

        # Return the utility values when the game gets over
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "noMove"

        # Get legal actions for the agent
        legalAction = gameState.getLegalActions()
        val = []
        act = []
        for action in legalAction:
            scoreVal, scoreAct = self.minFunction(gameState.generateSuccessor(self.index, action), depth, 1)
            val.append(scoreVal)
            act.append(scoreAct)
        alpha = max(val)
        # Find the index of the maximum value among the children
        for i in range(len(val)):
            if val[i] == alpha: \
                    alphaIdx = i
        bestIndex = alphaIdx
        return alpha, legalAction[bestIndex]

    def minFunction(self, gameState, depth, agent):
        """
        minFunction recursively computes the average value of sum of all its children
        The traversal is done from the root till the leaves in the depth first search manner
        and the values are returned all the way to the top. This function will be executed by each MIN agent
        and the average value of all its options is taken.
        This is done until the terminal states are reached where the function is the utility value.
        """

        # Return the utility value when the game gets over
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "noMove"
        # Get the number of agents, number of ghosts here
        ghostCount = gameState.getNumAgents() - 1
        # Get legal actions for the agents
        legalAction = gameState.getLegalActions(agent)
        val = []
        act = []
        # Determine if the next move is Max move or Min agent move
        if agent != ghostCount:
            for action in legalAction:
                scoreVal ,  scoreAct = self.minFunction(gameState.generateSuccessor(agent, action), depth, agent + 1)
                val.append(scoreVal)
                act.append(scoreAct)
        else:
            for action in legalAction:
                scoreVal, scoreAct = self.maxFunction(gameState.generateSuccessor(agent, action), (depth - 1))
                val.append(scoreVal)
                act.append(scoreAct)
        valSum = 0
        # Find the average of the value of the children
        for i in range(len(val)):
            valSum += val[i]
        beta = valSum / len(val)
        leastIndex = random.randint(0, len(val) - 1)
        return beta, legalAction[leastIndex]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

