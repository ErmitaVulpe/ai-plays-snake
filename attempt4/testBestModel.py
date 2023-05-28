import math
import ai4
import snake
import time
import sys
sys.setrecursionlimit(10**6)

def snakeDriver(model):
    snakeInstance = snake.snakeGame(40, 40, True)
    isGameOver = False

    while not isGameOver:
        networkInput = [snakeInstance.direction]

        headPosition = snakeInstance.snakePosition[0]
        match snakeInstance.direction:
            case 1:
                headNeighbours = {
                    "left": [headPosition[0], headPosition[1] - 1],
                    "forward": [headPosition[0] - 1, headPosition[1]],
                    "right": [headPosition[0], headPosition[1] + 1]
                }
            case 2:
                headNeighbours = {
                    "left": [headPosition[0] - 1, headPosition[1]],
                    "forward": [headPosition[0], headPosition[1] + 1],
                    "right": [headPosition[0] + 1, headPosition[1]]
                }
            case 3:
                headNeighbours = {
                    "left": [headPosition[0], headPosition[1] + 1],
                    "forward": [headPosition[0] + 1, headPosition[1]],
                    "right": [headPosition[0], headPosition[1] - 1]
                }
            case 4:
                headNeighbours = {
                    "left": [headPosition[0] + 1, headPosition[1]],
                    "forward": [headPosition[0], headPosition[1] - 1],
                    "right": [headPosition[0] - 1, headPosition[1]]
                }
            case _:
                headNeighbours = {}

        obstacles = [0, 0, 0]
        for index, value in enumerate(headNeighbours):
            if headNeighbours[value][0] < 0 or headNeighbours[value][0] == snakeInstance.fieldWidth or headNeighbours[value][1] < 0 or headNeighbours[value][1] == snakeInstance.fieldHeight:
                obstacles[index] = 1
                continue

            if headNeighbours[value] in snakeInstance.snakePosition: obstacles[index] = 1

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
                if not is_valid_position(row, col) or field[row][col] != 0:
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
        
        for index, value in enumerate(headNeighbours):
            if headNeighbours[value][0] < 0 or headNeighbours[value][0] == snakeInstance.fieldWidth or headNeighbours[value][1] < 0 or headNeighbours[value][1] == snakeInstance.fieldHeight:
                networkInput += [0]
                continue
            fieldCopy = snakeInstance.field.copy()
            fieldCopy[headNeighbours[value][0]][headNeighbours[value][1]] = 1
            networkInput += [(1 if isFieldSplit(fieldCopy) else 0)]


        def calculate_angle(x1, y1, foodx, foody, direction):
            angle_to_food = math.atan2(foody - y1, foodx - x1)
            direction_radians = math.radians((direction) * 90)
            
            # Calculate the difference in angles
            angle_difference = math.degrees(angle_to_food - direction_radians) - 90
            
            # Adjust the angle to be within the range of -180 to 180 degrees
            if angle_difference > 180:
                angle_difference -= 360
            elif angle_difference < -180:
                angle_difference += 360
            return - angle_difference
        
        angle = calculate_angle(headPosition[0], headPosition[1], snakeInstance.foodX, snakeInstance.foodY, snakeInstance.direction)

        if angle == 0: networkInput += [0, 0, 0, 0]
        elif angle == 180: networkInput += [1, 1, 1, 1]
        elif angle > 0: networkInput += [0, 1, 0, angle / 180]
        elif angle < 0: networkInput += [1, 0, - angle / 180, 0]

        networkOutput = model.forward(networkInput)
        isGameOver = snakeInstance.gameLoop(networkOutput.index(max(networkOutput)) + 1)

        time.sleep(0.1)
    


model = ai4.load("best_model.pickle")
snakeDriver(model)
print(model.score)