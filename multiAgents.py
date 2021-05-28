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


from pacman import GameState
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    #################################################################### NOT IMPLEMENTED 
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
    #################################################################### IMPLEMENTED
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        return self.minimax(0, 0, True, gameState)[0]
        
    def minimax(self, currentDepth, agentIndex, isMax, gameState):
        # During recursion, if agentIndex exceeded number of players
        allPlayedPerCurrentDepth = (agentIndex >= gameState.getNumAgents())

        # If it is pacman's turn again, set it
        agentIndex = 0 if allPlayedPerCurrentDepth else agentIndex
        # If all agents (pacman + all ghosts) got to play in a given depth, increase also the currentDepth
        currentDepth = (currentDepth + 1) if allPlayedPerCurrentDepth else currentDepth

        # If we reached the max tree depth, won, or lost
        if ((currentDepth == self.depth) or gameState.isWin() or gameState.isLose()):
            return [None, self.evaluationFunction(gameState)]

        # Recursion
        if (isMax):
            return self.handleMaximazer(currentDepth, agentIndex, gameState)
        else:
            return self.handleMinimizer(currentDepth, agentIndex, gameState)

    def handleMaximazer(self, currentDepth, agentIndex, gameState): 
        actions = gameState.getLegalActions(agentIndex)
        scores = []

        for action in actions: 
            # Minimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            score = self.minimax(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState)[1]
            scores.append(score)

        # Return preparation
        bestScore = max(scores)
        bestActionsIndex = scores.index(bestScore)
        bestAction = actions[bestActionsIndex]

        return [bestAction, bestScore]

    def handleMinimizer(self, currentDepth, agentIndex, gameState): 
        actions = gameState.getLegalActions(agentIndex)
        scores = []

        for action in actions: 
            # Minimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            score = self.minimax(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState)[1]
            scores.append(score)

        # Return preparation
        bestScore = min(scores)
        bestActionsIndex = scores.index(bestScore)
        bestAction = actions[bestActionsIndex]

        return [bestAction, bestScore]

class AlphaBetaAgent(MultiAgentSearchAgent):
    #################################################################### IMPLEMENTED 
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        return self.minimaxPrune(0, 0, True, gameState)[0]
        
    def minimaxPrune(self, currentDepth, agentIndex, isMax, gameState, alpha=float('-inf'), beta=float('inf')):
        # During recursion, if agentIndex exceeded number of players
        allPlayedPerCurrentDepth = (agentIndex >= gameState.getNumAgents())

        # If it is pacman's turn again, set it
        agentIndex = 0 if allPlayedPerCurrentDepth else agentIndex
        # If all agents (pacman + all ghosts) got to play in a given depth, increase also the currentDepth
        currentDepth = (currentDepth + 1) if allPlayedPerCurrentDepth else currentDepth

        # If we reached the max tree depth, won, or lost
        if ((currentDepth == self.depth) or gameState.isWin() or gameState.isLose()):
            return [None, self.evaluationFunction(gameState)]

        # Recursion
        if (isMax):
            return self.handleMaximazer(currentDepth, agentIndex, gameState, alpha, beta)
        else:
            return self.handleMinimizer(currentDepth, agentIndex, gameState, alpha, beta)

    def handleMaximazer(self, currentDepth, agentIndex, gameState, alpha, beta): 
        actions = gameState.getLegalActions(agentIndex)
        bestScore = float('-inf')
        scores = []

        for action in actions: 
            # Minimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            score = self.minimaxPrune(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState, alpha, beta)[1]
            scores.append(score)

            # Adjusting best score for comparison to alfa max
            bestScore = max(scores)

            # Pruning handling
            alpha = max(alpha, bestScore)
            if alpha > beta: 
                break

        # Return preparation
        bestActionsIndex = scores.index(bestScore)
        bestAction = actions[bestActionsIndex]

        return [bestAction, bestScore]

    def handleMinimizer(self, currentDepth, agentIndex, gameState, alpha, beta): 
        actions = gameState.getLegalActions(agentIndex)
        bestScore = float('inf')
        scores = []

        for action in actions: 
            # Minimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            score = self.minimaxPrune(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState, alpha, beta)[1]
            scores.append(score)

            # Adjusting best score for comparison to beta min
            bestScore = min(scores)

            # Pruning handling
            beta = min(beta, bestScore)
            if beta < alpha: 
                break

        # Return preparation
        bestActionsIndex = scores.index(bestScore)
        bestAction = actions[bestActionsIndex]

        return [bestAction, bestScore]


class ExpectimaxAgent(MultiAgentSearchAgent):
    #################################################################### IMPLEMENTED (getAction only)
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        return self.expectimax(0, 0, True, gameState)[0]
        
    def expectimax(self, currentDepth, agentIndex, isMax, gameState):
        # During recursion, if agentIndex exceeded number of players
        allPlayedPerCurrentDepth = (agentIndex >= gameState.getNumAgents())

        # If it is pacman's turn again, set it
        agentIndex = 0 if allPlayedPerCurrentDepth else agentIndex
        # If all agents (pacman + all ghosts) got to play in a given depth, increase also the currentDepth
        currentDepth = (currentDepth + 1) if allPlayedPerCurrentDepth else currentDepth

        # If we reached the max tree depth, won, or lost
        if ((currentDepth == self.depth) or gameState.isWin() or gameState.isLose()):
            return [None, self.evaluationFunction(gameState)]

        # Recursion
        if (isMax):
            return self.handleMaximazer(currentDepth, agentIndex, gameState)
        else:
            return self.handleProb(currentDepth, agentIndex, gameState)

    def handleMaximazer(self, currentDepth, agentIndex, gameState): 
        actions = gameState.getLegalActions(agentIndex)
        scores = []

        for action in actions: 
            # Minimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            score = self.expectimax(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState)[1]
            scores.append(score)

        # Return preparation
        bestScore = max(scores)
        bestActionsIndex = scores.index(bestScore)
        bestAction = actions[bestActionsIndex]

        return [bestAction, bestScore]

    def handleProb(self, currentDepth, agentIndex, gameState): 
        actions = gameState.getLegalActions(agentIndex)
        scores = []

        # Return preparation
        action = None
        score = 0.0

        # Scores are later adjusted based on the probability of the action
        prob = 1.0/len(actions)

        for actionItem in actions: 
            # expectimax parameter preparation
            nextGameState = gameState.generateSuccessor(agentIndex, actionItem)
            nextAgentIndex = agentIndex + 1
            nextAgentIsMax = (nextAgentIndex == 0) or (nextAgentIndex >= gameState.getNumAgents())

            # Score handling
            scoreItem = self.expectimax(currentDepth, nextAgentIndex, nextAgentIsMax, nextGameState)[1]
            scores.append(scoreItem)
            action = actionItem

        # Summarize the score with its probabilities
        for x, storedScore in enumerate(scores):
            score += prob * storedScore

        return [action, score]

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
