import numpy
import random
import os

class snakeGame:
    def __init__(self, width: int, height: int, visible: bool = False) -> None:
        if width < 4 or height < 4: raise ValueError("Field area is too small")
        self.gameOver = False
        self.fieldWidth = width
        self.fieldHeight = height
        self.direction = 1
        self.score = 1
        self.field = numpy.zeros((self.fieldWidth, self.fieldHeight), dtype=int)
        self.foodX = random.randint(0, self.fieldWidth - 1)
        self.foodY = random.randint(0, self.fieldHeight - 1)
        self.snakePosition = [(self.fieldWidth // 2, self.fieldHeight // 2)]
        self.visible = visible
        # self.

        self.mapSnake()
        self.addFood()

    def mapSnake(self):
        for index, snakeBlock in enumerate(self.snakePosition):
            if index == 0: self.field[snakeBlock[0]][snakeBlock[1]] = 2
            else: self.field[snakeBlock[0]][snakeBlock[1]] = 1

    def addFood(self):
        while self.field[self.foodX][self.foodY] != 0:
            self.foodX = random.randint(0, self.fieldWidth - 1)
            self.foodY = random.randint(0, self.fieldHeight - 1)
        self.field[self.foodX][self.foodY] = 3

    def renderGame(self):
        # ANSI codes
        background = "\033[34;0;44m   " # Blue
        body = "\033[30;0;40m   " # Black
        head = "\033[31;0;41m   " # Red
        food = "\033[32;0;42m   " # Green

        os.system('cls')

        for rows in self.field:
            # print(f"row = {row}")
            for tile in rows:
                # print(tile)
                match tile:
                    case 0: print(background, end="")
                    case 1: print(body, end="")
                    case 2: print(head, end="")
                    case 3: print(food, end="")
            print("\033[0m")

    def gameLoop(self, newDirection: int) -> bool:
        """
        Call this function for a game tick

        Parameters:
            - newDirection (int): the new direction for the snake to turn:
                - 1 - Up
                - 2 - Right
                - 3 - Down
                - 4 - Left

        Returns (bool): True if the game ends
        """
        if self.gameOver: return print("Bruh the game is already over")
        if newDirection < 1 or newDirection > 4: return print("Direction out of range. (1 - 4)")
        if newDirection + 2 == self.direction or newDirection - 2 == self.direction:
            newDirection = self.direction
        else: self.direction = newDirection

        headPosition = self.snakePosition[0]
        self.field[headPosition[0]][headPosition[1]] = 1
        match self.direction:
            case 1: newHead = (headPosition[0] - 1, headPosition[1])
            case 2: newHead = (headPosition[0], headPosition[1] + 1)
            case 3: newHead = (headPosition[0] + 1, headPosition[1])
            case 4: newHead = (headPosition[0], headPosition[1] - 1)

        if newHead[0] < 0 or newHead[0] >= self.fieldHeight or \
           newHead[1] < 0 or newHead[1] >= self.fieldWidth or \
           newHead in self.snakePosition:
            return True

        if newHead == (self.foodX, self.foodY):
            self.score += 1
            self.addFood()
        else:
            oldTile = self.snakePosition.pop(-1)
            self.field[oldTile[0]][oldTile[1]] = 0


        self.snakePosition.insert(0, (newHead[0], newHead[1]))
        self.field[newHead[0]][newHead[1]] = 2

        if self.visible: self.renderGame()
        return False






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






if __name__ == "__main__":
    # snakeInstance = snakeGame(11, 11, True)

    # snakeInstance.renderGame()
    # isGameOver = False
    # while not isGameOver:
    #     isGameOver = snakeInstance.gameLoop(int(input()))

    field = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ] # False
    print("Should be False, is ", isFieldSplit(field))

    field = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ]  # True
    print("Should be True, is  ", isFieldSplit(field))

    field = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ] # True
    print("Should be True, is  ", isFieldSplit(field))

    field = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0]
    ] # False
    print("Should be False, is ", isFieldSplit(field))

    field = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 0]
    ] # True
    print("Should be True, is  ", isFieldSplit(field))

    field = [
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0]
    ] # False
    print("Should be False, is ", isFieldSplit(field))

    field = [
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ] # True
    print("Should be True, is  ", isFieldSplit(field))

    field = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ] # True
    print("Should be True, is  ", isFieldSplit(field))

    field = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ] # False
    print("Should be False, is ", isFieldSplit(field))





