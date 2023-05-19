import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
display_width = 600
display_height = 400
 
display = pygame.display.set_mode((display_width, display_height))
 
clock = pygame.time.Clock()
 
snake_block_size = 10
snake_speed = 20
 
font_style = pygame.font.SysFont("bahnschrift", 25)
 
 
def Your_score(score):
    pygame.display.set_caption("Your Score: " + str(score))
 
 
 
def our_snake(snake_block, snake_list, snake_Head):
    for x in snake_list:
        if x == snake_Head:
            pygame.draw.rect(display, red, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])
 
 
def gameLoop():
    game_over = False
    game_close = False
 
    x1 = display_width / 2
    y1 = display_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    score = 0
 
    foodx = round(random.randrange(0, display_width - snake_block_size) / snake_block_size) * snake_block_size
    foody = round(random.randrange(0, display_height - snake_block_size) / snake_block_size) * snake_block_size
 
    while not game_over:
 
        while game_close == True:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score = Length_of_snake - 1
            Your_score(score)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    
        button = None
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    button = "left"
                elif event.key == pygame.K_RIGHT:
                    button = "right"
                elif event.key == pygame.K_UP:
                    button = "up"
                elif event.key == pygame.K_DOWN:
                    button = "down"

        if button == "left":
            x1_change = -snake_block_size
            y1_change = 0
        elif button == "right":
            x1_change = snake_block_size
            y1_change = 0
        elif button == "up":
            y1_change = -snake_block_size
            x1_change = 0
        elif button == "down":
            y1_change = snake_block_size
            x1_change = 0
 
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        display.fill(blue)
        pygame.draw.rect(display, green, [foodx, foody, snake_block_size, snake_block_size])
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
        Your_score(score)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block_size) / 10.0) * 10.0
            Length_of_snake += 1

        def snakeListParse(bigList):
            return [[int(x / 10) for x in sublist] for sublist in bigList][::-1]


        print(snakeListParse(snake_List))
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()