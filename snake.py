import pygame, random, pygame_menu
from pygame.locals import *

#Sizes
block = 20
screen_pixels = 800

# Helper functions
def set_size(value, size):
    global block
    block = value[0][1]

def on_grid_random():
    x = random.randint(0,(screen_pixels-block)//block)
    y = random.randint(0,(screen_pixels-block)//block)
    print(x)
    return (x * block, y * block)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def game():
    global snake, my_direction, apple_pos, score, game_over, screen
    clock.tick(20)
    snake_skin = pygame.Surface((block,block))
    snake_skin.fill((255,255,255)) #White

    apple = pygame.Surface((block,block))
    apple.fill((255,0,0))


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0,0))
        score = score + 1
        
    # Check if snake collided with boundaries
    if snake[0][0] == screen_pixels or snake[0][1] == screen_pixels or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True
        return None
    
    # Check if the snake has hit itself
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True
            return None

    if game_over:
        return None
    
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
        
    # Actually make the snake move.
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - block)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + block)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + block, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - block, snake[0][1])
    
    screen.fill((0,0,0))
    screen.blit(apple, apple_pos)
    
    for x in range(0, screen_pixels, block): # Draw vertical lines
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, screen_pixels))
    for y in range(0, screen_pixels, block): # Draw vertical lines
        pygame.draw.line(screen, (40, 40, 40), (0, y), (screen_pixels, y))
    
    score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (screen_pixels - 120, block)
    screen.blit(score_font, score_rect)
    
    for pos in snake:
        screen.blit(snake_skin,pos)

    pygame.display.update()


def interaction():
    global game_over, score, snake, screen, start, apple_pos
    game_over = False

    snake = [(200, 200), (200 + block, 200), (220 + 2*block,200)]
    
    apple_pos = on_grid_random()

    while not game_over:
        game()

    while game_over:
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (screen_pixels / 2, block)
        screen.blit(game_over_screen, game_over_rect)

        game_over_font = pygame.font.Font('freesansbold.ttf', 25)
        game_over_screen = game_over_font.render('Press SPACEBAR to try again', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (screen_pixels / 2, 100)


        screen.blit(game_over_screen, game_over_rect)

        pygame.display.update()
        pygame.time.wait(500)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    if event.key == K_SPACE:
                        score = 0
                        return None

def menu():
    menu = pygame_menu.Menu('Welcome', screen_pixels, screen_pixels,
                       theme=pygame_menu.themes.THEME_DARK)

    menu.add.text_input('Name: ', default='Player01')
    menu.add.selector('Size :', [('Small', 10), ('Medium', 20), ('Large', 30)], onchange=set_size)
    menu.add.button('Play', interaction)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

# Macro definition for snake movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


pygame.init()

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

start = False

screen = pygame.display.set_mode((screen_pixels, screen_pixels))
pygame.display.set_caption('Snake')

if __name__ == '__main__':
    while True:
        menu()