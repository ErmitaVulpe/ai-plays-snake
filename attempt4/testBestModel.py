import math
import ai4
import snake
import time
import sys
sys.setrecursionlimit(10**6)

def snakeDriver(model):
    snakeInstance = snake.snakeGame(10, 10, True)
    isGameOver = False

    def isFieldSplit(field):
        # ChatGPT go brr
        rows = len(field)
        cols = len(field[0])

        # Helper function to check if a position is valid within the field
        def is_valid_position(row, col):
            return 0 <= row < rows and 0 <= col < cols

        # Helper function to perform a depth-first search (DFS)
        def dfs(row, col):
            if not is_valid_position(row, col) or (field[row][col] != 0 and field[row][col] != 3):
                return

            field[row][col] = -1  # Mark the current position as visited

            # Perform DFS on adjacent positions
            dfs(row - 1, col)  # Up
            dfs(row + 1, col)  # Down
            dfs(row, col - 1)  # Left
            dfs(row, col + 1)  # Right

        # Find the first zero position and perform DFS
        for i in range(rows):
            for j in range(cols):
                if field[i][j] == 0:
                    dfs(i, j)
                    break
            else:
                continue
            break

        # Check if there are any unvisited zero positions left
        for i in range(rows):
            for j in range(cols):
                if field[i][j] == 0:
                    return True

        return False
    
    def checkIfFieldWillSplit(neightbour, twoStepsAhead):
        if neightbour[0] < 0 or neightbour[0] >= snakeInstance.fieldWidth or neightbour[1] < 0 or neightbour[1] >= snakeInstance.fieldHeight:
            return 1
        fieldCopy = snakeInstance.field.copy()
        fieldCopy[neightbour[0]][neightbour[1]] = 1
        lastSnakePart = snakeInstance.snakePosition[-1]
        fieldCopy[lastSnakePart[0]][lastSnakePart[1]] = 0
        if twoStepsAhead: fieldCopy[snakeInstance.snakePosition[-2][0]][snakeInstance.snakePosition[-2][1]] = 0
        return (1 if isFieldSplit(fieldCopy) else 0)

    def calculate_angle(x, y, foodx, foody):
        dx = x - foodx
        dy = y - foody
        angle = math.degrees(math.atan2(dy, dx))
        angle = ((angle - 90) % 360)
        return angle
    
    def checkForObstacles(tileCoords):
        if tileCoords[0] < 0 or tileCoords[0] >= snakeInstance.fieldWidth or tileCoords[1] < 0 or tileCoords[1] >= snakeInstance.fieldHeight or tileCoords in snakeInstance.snakePosition: return 1
        else: return 0

    # ---

    while not isGameOver:
        networkInput = []
        headPosition = snakeInstance.snakePosition[0]
        

        # I know this looks awful but its sadly more efficient to do it like this instead of nested loops
        obstacles = [[] for _ in range(8)]
        nextMovesSplitTheField = [[] for _ in range(8)]
        visionRange = 4
        for i in range(1, visionRange + 1): 
            neighbor = (headPosition[0], headPosition[1] - i)
            obstacles[0].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[0].append(checkIfFieldWillSplit(neighbor, False))

            neighbor = (headPosition[0] + i, headPosition[1] - i)
            obstacles[1].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[1].append(checkIfFieldWillSplit(neighbor, True))

            neighbor = (headPosition[0] + i, headPosition[1])
            obstacles[2].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[2].append(checkIfFieldWillSplit(neighbor, False))

            neighbor = (headPosition[0] + i, headPosition[1] + i)
            obstacles[3].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[3].append(checkIfFieldWillSplit(neighbor, True))

            neighbor = (headPosition[0], headPosition[1] + i)
            obstacles[4].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[4].append(checkIfFieldWillSplit(neighbor, False))

            neighbor = (headPosition[0] - i, headPosition[1] + i)
            obstacles[5].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[5].append(checkIfFieldWillSplit(neighbor, True))

            neighbor = (headPosition[0] - i, headPosition[1])
            obstacles[6].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[6].append(checkIfFieldWillSplit(neighbor, False))

            neighbor = (headPosition[0] - i, headPosition[1] - i)
            obstacles[7].append(checkForObstacles(neighbor))
            nextMovesSplitTheField[7].append(checkIfFieldWillSplit(neighbor, True))

        obstacles = [item for sublist in obstacles for item in sublist]
        networkInput += obstacles
        nextMovesSplitTheField = [item for sublist in nextMovesSplitTheField for item in sublist]
        networkInput += nextMovesSplitTheField

        
        # Get angles to the food
        angle = calculate_angle(headPosition[0], headPosition[1], snakeInstance.foodX, snakeInstance.foodY)
        shiftedAngle = angle + 45
        anglesRounded = []
        anglesPrecise = []

        for direction in range(4):
            angleFormASide = shiftedAngle - (direction * 90)
            if angleFormASide >= 0 and angleFormASide <= 90: 
                anglesRounded.append(1)
                anglesPrecise.append((angleFormASide - 45) / 45)
            else: 
                anglesRounded.append(0)
                anglesPrecise.append(0)
        networkInput += anglesRounded + anglesPrecise

        networkOutput = model.forward(networkInput)
        moveDirection = networkOutput.index(max(networkOutput)) + 1
        print(f"obstacles: {obstacles}")
        print(f"nextMovesSplitTheField: {nextMovesSplitTheField}")
        print(f"anglesRounded: {anglesRounded}")
        print(f"anglesPrecise: {anglesPrecise}")
        # moveDirection = int(input())
        isGameOver = snakeInstance.gameLoop(moveDirection)

        time.sleep(0.05)
    


model = ai4.load("best_model.pickle")
# model = ai4.load("trainingModels.pickle")[-1]
snakeDriver(model)
# input()
print(model.score)
print(model)