import time

class PuzzleNode:
    def __init__(self, board, g, previousNode):
        self.board = board
        self.previousNode = previousNode
        self.g = g
        self.h = self.getH()

    def getH(self):
        hValue = 9
        for index, number in enumerate(self.board):
            if number != None and number == index + 1:
                hValue -= 1

        if self.board.index(None) == 8:
            hValue -= 1

        return hValue

    def getF(self):
        return self.g + self.h
    
    def toString(self):
        return str(self.board)
    
    def isEqual(self, puzzleNode):
        return puzzleNode.toString() == self.toString()

    def getPath(self):
        if self.previousNode:
            return [self.previousNode.toString()] + self.previousNode.getPath()
        
        return []

def isFinished(puzzleNode):
    final_node = [1, 2, 3, 4, 5, 6, 7, 8, None]
    finishedNode = PuzzleNode(final_node, 0, None)
    return puzzleNode.isEqual(finishedNode)

def getActionsFromPuzzleNode(puzzleNode):
    derivedNodes = []
    indexOfStar = puzzleNode.board.index(None)

    if indexOfStar in [0, 1, 2, 3, 4, 5]:
        derivedNodes.append(getDerivedNodesFromAction(puzzleNode, 'down'))

    if indexOfStar in [3, 4, 5, 6, 7, 8]:
        derivedNodes.append(getDerivedNodesFromAction(puzzleNode, 'up'))

    if indexOfStar in [0, 1, 3, 4, 6, 7]:
        derivedNodes.append(getDerivedNodesFromAction(puzzleNode, 'right'))

    if indexOfStar in [1, 2, 4, 5, 7, 8]:
        derivedNodes.append(getDerivedNodesFromAction(puzzleNode, 'left'))

    return derivedNodes

def getDerivedNodesFromAction(puzzleNode, action):
    indexOfStar = puzzleNode.board.index(None)

    if action == 'up':
        derivedPuzzleNode = puzzleNode.board[:]
        movedPiece = derivedPuzzleNode[indexOfStar - 3]
        derivedPuzzleNode[indexOfStar - 3] = None
        derivedPuzzleNode[indexOfStar] = movedPiece

        return PuzzleNode(derivedPuzzleNode, puzzleNode.g + 1, puzzleNode)

    if action == 'left':
        derivedPuzzleNode = puzzleNode.board[:]
        movedPiece = derivedPuzzleNode[indexOfStar - 1]
        derivedPuzzleNode[indexOfStar - 1] = None
        derivedPuzzleNode[indexOfStar] = movedPiece

        return PuzzleNode(derivedPuzzleNode, puzzleNode.g + 1, puzzleNode)

    if action == 'right':
        derivedPuzzleNode = puzzleNode.board[:]
        movedPiece = derivedPuzzleNode[indexOfStar + 1]
        derivedPuzzleNode[indexOfStar + 1] = None
        derivedPuzzleNode[indexOfStar] = movedPiece

        return PuzzleNode(derivedPuzzleNode, puzzleNode.g + 1, puzzleNode)

    if action == 'down':
        derivedPuzzleNode = puzzleNode.board[:]
        movedPiece = derivedPuzzleNode[indexOfStar + 3]
        derivedPuzzleNode[indexOfStar + 3] = None
        derivedPuzzleNode[indexOfStar] = movedPiece

        return PuzzleNode(derivedPuzzleNode, puzzleNode.g + 1, puzzleNode)

def printResults(startTime, resultPuzzleNode, createdNodes):
    endTime = time.time()
    resultPath = resultPuzzleNode.getPath()
    print('Problem solved. Stats:')
    print(f"Time taken: {endTime - startTime:.10f}")
    print('Number of visited nodes:',len(visitedPuzzleNodes))
    print('Path length:', len(resultPath))
    print(f"path: {[p for p in resultPath[::-1]]}")

def isVisitedNode(puzzleNode):
    return any(visitedNode.isEqual(puzzleNode) for visitedNode in visitedPuzzleNodes)

visitedPuzzleNodes = []
borderPuzzleNodes = []

def aStarSearch(initialValue):
    START_TIME = time.time()
    RESULT_PUZZLE_NODE = None
    CREATED_NODES = 1
    initialNode = PuzzleNode(initialValue, 0, None)
    print(f'\nStart state: {initialNode.toString()}')

    if isFinished(initialNode):
        RESULT_PUZZLE_NODE = initialNode
        printResults(START_TIME, RESULT_PUZZLE_NODE, CREATED_NODES)
        return print('First node is the solution!')

    borderPuzzleNodes.append(initialNode)

    while borderPuzzleNodes:
        actualPuzzleNode = borderPuzzleNodes.pop(0)
        if isFinished(actualPuzzleNode):
            RESULT_PUZZLE_NODE = actualPuzzleNode
            break

        visitedPuzzleNodes.append(actualPuzzleNode)

        derivedPuzzleNodes = getActionsFromPuzzleNode(actualPuzzleNode)

        for derivedPuzzleNode in derivedPuzzleNodes:
            if isVisitedNode(derivedPuzzleNode):
                continue
            borderPuzzleNodes.append(derivedPuzzleNode)
            borderPuzzleNodes.sort(key = lambda x: x.getF())
            CREATED_NODES += 1

    return printResults(START_TIME, RESULT_PUZZLE_NODE, CREATED_NODES)


