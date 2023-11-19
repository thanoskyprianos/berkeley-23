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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        from util import manhattanDistance

        for i, ghost in enumerate(successorGameState.getGhostPositions()):
            
            new_dist = manhattanDistance(newPos, ghost)
            cur_dist = manhattanDistance(currentGameState.getPacmanPosition(), ghost)
            if newScaredTimes[i] > 0:
                if new_dist - cur_dist < 0:            # if we move closer to ghost
                    if new_dist < newScaredTimes[i]:
                        return float('inf')
                    else:                              # else check for other options
                        continue
            else:
                if new_dist <= 2:                      # if ghost is hostile and we are relatively close, avoid it
                    return float('-inf')

        for capsule in currentGameState.getCapsules(): # prefer to go on capsule before checking food
            if capsule == newPos:
                return float('inf')
            
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            return float('inf')
        
        # as a last option try find the closest capsule (if there is any) or food
        # and pass the negation of it, as we prefer higher values
        
        closest_food = min(manhattanDistance(newPos, food) for food in newFood.asList())
        try:
            closest_capsule = min(manhattanDistance(newPos, capsule) for capsule in currentGameState.getCapsules())
            return -min(closest_food, closest_capsule)
        except ValueError:
            return -closest_food

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        
        def minValue(index : int, depth : int, state : GameState) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v = float('inf')
            for action in state.getLegalActions(index):
                if index == state.getNumAgents() - 1: # switch to pacman on last ghost (depth += 1)
                    v = min(v, maxValue(depth + 1, state.generateSuccessor(index, action))) 
                else:                                 # else continue with next ghost (index += 1)
                    v = min(v, minValue(index + 1, depth, state.generateSuccessor(index, action)))

            return v
    
        def maxValue(depth : int, state : GameState) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v = float('-inf')
            for action in state.getLegalActions():
                v = max(v, minValue(1, depth, state.generateSuccessor(0, action))) # start with index 1 : first ghost

            return v

        # return the max min-value action of root's (MAX's) successors (MAX plays first)
        return max (
            gameState.getLegalActions(),
            key = lambda action:
                minValue(1, 0, gameState.generateSuccessor(0, action)) # 1 : first ghost, 0 : first depth    
        )

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def maxValue(depth : int, state : GameState, a : float, b : float) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v = float('-inf')
            for action in state.getLegalActions():
                v = max(v, minValue(1, depth, state.generateSuccessor(0, action), a, b))
                if v > b: return v
                a = max(a, v)

            return v


        def minValue(index : int, depth : int, state : GameState, a : float, b : float) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)

            v = float('inf')
            for action in state.getLegalActions(index):
                if index == state.getNumAgents() - 1:
                    v = min(v, maxValue(depth + 1, state.generateSuccessor(index, action), a, b))
                else:
                    v = min(v, minValue(index + 1, depth, state.generateSuccessor(index, action), a, b))

                if v < a: return v
                b = min(b, v)
            
            return v

        max_action = None
        max_v = a = float('-inf')
        b = float('inf')

        for action in gameState.getLegalActions():
            v = minValue(1, 0, gameState.generateSuccessor(0, action), a, b)
            if v > max_v:
                max_v = v
                max_action = action
                a = max(a, v)       # set new lower bound

        return max_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        def maxValue(depth : int, state : GameState) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v = float('-inf')
            for action in state.getLegalActions():
                v = max(v, expectedValue(1, depth, state.generateSuccessor(0, action)))
            
            return v

        def expectedValue(index : int, depth : int, state : GameState) -> float:
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            
            s = 0
            actions = state.getLegalActions(index)

            for action in actions:
                if index == state.getNumAgents() - 1:
                    s += maxValue(depth + 1, state.generateSuccessor(index, action))
                else:
                    s += expectedValue(index + 1, depth, state.generateSuccessor(index, action))

            return (1 / len(actions)) * s # P(r) = 1 / # of legal actions

        return max (
            gameState.getLegalActions(),
            key= lambda action:
                expectedValue(1, 0, gameState.generateSuccessor(0, action))
        )   

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
