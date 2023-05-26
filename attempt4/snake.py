import numpy
import random

gameOver = False

fieldWidth = 6
fieldHeight = 4
filed = numpy.zeros((fieldWidth, fieldHeight))
print(filed)

foodX = 0
foodY = 0

def addFood():
    foodX = random.randint(0, fieldWidth - 1)

addFood()
# while not gameOver:
#     pass