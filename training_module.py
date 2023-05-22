import pygame
import random
import math

def trainingInstance(modelList):
    selectedModel = None

    pygame.init()

    colors = {
        "white": (255, 255, 255, 255),
        "yellow": (255, 255, 102, 255),
        "black": (0, 0, 0, 255),
        "red": (213, 50, 80, 255),
        "green": (0, 255, 0, 255),
        "blue": (50, 153, 213, 255)
    }
    
    snake_block_size = 10
    snake_speed = 999999999999999999999999

    display_width = 60 * snake_block_size
    display_height = 40 * snake_block_size
    
    display = pygame.display.set_mode((display_width, display_height))
    
    clock = pygame.time.Clock()
    
    font_style = pygame.font.SysFont("bahnschrift", 25)
    
    
    def Your_score(score):
        pygame.display.set_caption("Your Score: " + str(score))
    
    
    
    def our_snake(snake_block, snake_list, snake_Head):
        for x in snake_list:
            if x == snake_Head:
                pygame.draw.rect(display, colors["red"], [x[0], x[1], snake_block, snake_block])
            else:
                pygame.draw.rect(display, colors["black"], [x[0], x[1], snake_block, snake_block])
    
    
    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        display.blit(mesg, [display_width / 6, display_height / 3])
    
    def gameLoop():
        game_over = False
        game_close = False
    
        x1 = display_width / 2
        y1 = display_height / 2
    
        direction = 0
        x1_change = 0
        y1_change = 0
    
        moveHistory = []
        snake_List = []
        Length_of_snake = 1
        score = 0
        button = 1
        movesSinceLastFood = 0
    
        foodx = round(random.randrange(0, display_width - snake_block_size) / snake_block_size) * snake_block_size
        foody = round(random.randrange(0, display_height - snake_block_size) / snake_block_size) * snake_block_size
    
        while not game_over:
            if game_close == True:
                selectedModel.score += (Length_of_snake - 1) * 10
                selectedModel.score += (5 / (math.sqrt(abs(x1 - foodx) ** 2 + abs(y1 - foody) ** 2)))
                break
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        button = 1
                    elif event.key == pygame.K_RIGHT:
                        button = 2
                    elif event.key == pygame.K_DOWN:
                        button = 3
                    elif event.key == pygame.K_LEFT:
                        button = 4

            if button != 0: 
                lolo = button - 2 if button + 2 > 4 else button + 2 
                if lolo == direction: continue
                direction = button

            match direction:
                case 1:
                    y1_change = -snake_block_size
                    x1_change = 0
                case 2:
                    x1_change = snake_block_size
                    y1_change = 0
                case 3:
                    y1_change = snake_block_size
                    x1_change = 0
                case 4:
                    x1_change = -snake_block_size
                    y1_change = 0
    
            if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            display.fill(colors["blue"])
            pygame.draw.rect(display, colors["green"], [foodx, foody, snake_block_size, snake_block_size])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
    
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
    
            our_snake(snake_block_size, snake_List, snake_Head)
            score = Length_of_snake - 1
            Your_score(10 *score)
    
            pygame.display.update()
    
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, display_width - snake_block_size) / 10.0) * 10.0
                foody = round(random.randrange(0, display_height - snake_block_size) / 10.0) * 10.0
                Length_of_snake += 1
                movesSinceLastFood = 0


            # Handle the network
            if snake_Head[0] < 0 or snake_Head[0] >= display_width or snake_Head[1] < 0 or snake_Head[1] >= display_height: 
                game_close = True
                selectedModel.score = -10
                continue

            match direction:
                case 1:
                    headNeighbours = {
                        "left": [x1 - snake_block_size, y1],
                        "forward": [x1, y1 - snake_block_size],
                        "right": [x1 + snake_block_size, y1]
                    }
                case 2:
                    headNeighbours = {
                        "left": [x1, y1 - snake_block_size],
                        "forward": [x1 + snake_block_size, y1],
                        "right": [x1, y1 + snake_block_size]
                    }
                case 3:
                    headNeighbours = {
                        "left": [x1 + snake_block_size, y1],
                        "forward": [x1, y1 + snake_block_size],
                        "right": [x1 - snake_block_size, y1]
                    }
                case 4:
                    headNeighbours = {
                        "left": [x1, y1 + snake_block_size],
                        "forward": [x1 - snake_block_size, y1],
                        "right": [x1, y1 - snake_block_size]
                    }
                case _:
                    headNeighbours = {}

            obstacles = [0, 0, 0]
            for index, value in enumerate(headNeighbours):
                headNeighbours[value][0] = int(headNeighbours[value][0] / snake_block_size)
                headNeighbours[value][1] = int(headNeighbours[value][1] / snake_block_size)

                if headNeighbours[value][0] < 0 or headNeighbours[value][0] == int(display_width / snake_block_size) or headNeighbours[value][1] < 0 or headNeighbours[value][1] == int(display_height / snake_block_size):
                    obstacles[index] = 1

                if obstacles[index] == 1: continue # doesn't check the color of tiles out of bounds
                if display.get_at((headNeighbours[value][0] * snake_block_size + int(snake_block_size / 2), headNeighbours[value][1] * snake_block_size + int(snake_block_size / 2))) == colors["black"]: obstacles[index] = 1

            # if len(headNeighbours) > 0:
            #     print(obstacles)

            def calculate_angle(x1, y1, foodx, foody, direction):
                angle_to_food = math.atan2(foody - y1, foodx - x1)
                direction_radians = math.radians((direction - 1) * 90)
                
                # Calculate the difference in angles
                angle_difference = math.degrees(angle_to_food - direction_radians) + 90
                
                # Adjust the angle to be within the range of -180 to 180 degrees
                if angle_difference > 180:
                    angle_difference -= 360
                elif angle_difference < -180:
                    angle_difference += 360
                return angle_difference
            
            angle = calculate_angle(x1, y1, foodx, foody, direction)

            if angle < -45 : adviseTurnDirection = -1
            elif angle <= 45: adviseTurnDirection = 0
            elif angle > 45: adviseTurnDirection = 1
            normalizedAngle = angle / 180
    

            networkInput = obstacles.copy()
            networkInput.insert(0, normalizedAngle)
            networkInput.insert(0, adviseTurnDirection)
            networkOutput = selectedModel.compute(networkInput)

            # moveHistory.append(highest_index)
            # if len(moveHistory) > 100:
            #     lastElement = moveHistory[-1]
            #     if all(element == lastElement for element in moveHistory[-100:]):
            #         print("IDIOT")
            #         selectedModel.score = -20
            #         break
            # # I've got a better idea

            movesSinceLastFood += 1
            if (movesSinceLastFood == (display_height / snake_block_size) * (display_width / snake_block_size)) or (len(snake_List) > 4 and movesSinceLastFood > (max(display_height / snake_block_size, display_width / snake_block_size))):
                # print("IDIOT")
                selectedModel.score = -20
                selectedModel.score += (Length_of_snake - 1) * 10
                selectedModel.score += (5 / (math.sqrt(abs(x1 - foodx) ** 2 + abs(y1 - foody) ** 2)))
                break

            highest_index = networkOutput.index(max(networkOutput))
            button += highest_index - 1
            if button == 0: button = 4
            elif button == 5: button = 1

            clock.tick(snake_speed)


    for model in modelList:
        selectedModel = model
        gameLoop()

    pygame.quit()
    return modelList