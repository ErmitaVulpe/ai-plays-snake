import math
import snake
import sys
sys.setrecursionlimit(10**6)

def snakeDriver(model):
    snakeInstance = snake.snakeGame(60, 40, False)
    isGameOver = False

    while not isGameOver:
        networkInput = []

        headPosition = snakeInstance.snakePosition[0]
        headNeighbours = [
            (headPosition[0], headPosition[1] - 1),
            (headPosition[0] + 1, headPosition[1]),
            (headPosition[0], headPosition[1] + 1),
            (headPosition[0] - 1, headPosition[1])
        ]

        obstacles = []
        for value in headNeighbours:
            if value[0] < 0 or value[0] == snakeInstance.fieldWidth or value[1] < 0 or value[1] == snakeInstance.fieldHeight or value in snakeInstance.snakePosition: obstacles.append(1)
            else: obstacles.append(0)

        networkInput += obstacles

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
        
        for neightbour in headNeighbours:
            if neightbour[0] < 0 or neightbour[0] == snakeInstance.fieldWidth or neightbour[1] < 0 or neightbour[1] == snakeInstance.fieldHeight:
                networkInput += [0]
                continue
            fieldCopy = snakeInstance.field.copy()
            fieldCopy[neightbour[0]][neightbour[1]] = 1
            lastSnakePart = snakeInstance.snakePosition[-1]
            fieldCopy[lastSnakePart[0]][lastSnakePart[1]] = 0
            networkInput += [(1 if isFieldSplit(fieldCopy) else 0)]


        def calculate_angle(x, y, foodx, foody):
            dx = x - foodx
            dy = y - foody
            angle = math.degrees(math.atan2(dy, dx))
            angle = ((angle - 90) % 360)
            return angle
        
        angle = calculate_angle(headPosition[0], headPosition[1], snakeInstance.foodX, snakeInstance.foodY)

        if angle >= 315 or angle <= 45: networkInput += [1, 0, 0, 0, angle / 360]
        elif angle > 45 and angle <= 135: networkInput += [0, 1, 0, 0, angle / 360]
        elif angle > 135 and angle < 225: networkInput += [0, 0, 1, 0, angle / 360]
        elif angle >= 225 and angle < 315: networkInput += [0, 0, 0, 1, angle / 360]

        networkOutput = model.forward(networkInput)
        moveDirection = networkOutput.index(max(networkOutput)) + 1
        isGameOver = snakeInstance.gameLoop(moveDirection)

        normalisedAngle = networkInput[-5:-1]
        if normalisedAngle[moveDirection - 1] == 1: model.score += 1
    model.score += snakeInstance.score * 10 + (1 / (math.sqrt(abs(headPosition[0] - snakeInstance.foodX) ** 2 + abs(headPosition[1] - snakeInstance.foodY) ** 2))) - 10


def trainingInstance(modelList):
    for model in modelList:
        snakeDriver(model)

    return modelList