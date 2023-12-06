import pygame
import time
import random

pygame.init()

# Sound Effects
crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load('jazz.mp3')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)

# Display settings
display_width = 800
display_height = 600
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

# Car settings
carImg = pygame.image.load('racecar.png')
car_width = 73

# Text settings
font_large = pygame.font.SysFont("comicsansms", 115)
font_medium = pygame.font.SysFont("comicsansms", 40)
font_small = pygame.font.SysFont("comicsansms", 20)

# TODO: Write a function called obstacles_dodged that displays the score.
def obstacles_dodged(count):
    score_text = font_medium.render("Dodged: " + str(count), True, black)
    window.blit(score_text, (10, 10))

def obstacles(obstaclex, obstacley, obstaclew, obstacleh, color):
    pygame.draw.rect(window, color, [obstaclex, obstacley, obstaclew, obstacleh])

def car(x, y):
    window.blit(carImg, (x, y))

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    large_text = pygame.font.SysFont("comicsansms", 115)
    text_surf, text_rect = text_objects("You Crashed", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    window.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again", 150, 450, 150, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(text_surf, text_rect)

def quitgame():
    pygame.quit()
    quit()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        TextSurf, TextRect = text_objects("A bit Racey", font_large)
        TextRect.center = ((display_width / 2), (display_height / 2))
        window.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    pygame.mixer.music.play(-1)

    car_x = (display_width * 0.45)
    car_y = (display_height * 0.8)
    x_change = 0

    obstacle_startx = random.randrange(0, display_width)
    obstacle_starty = -600
    obstacle_speed = 4
    obstacle_width = 100
    obstacle_height = 100

    # TODO: Make a variable to track the score (i.e., how many obstacles were dodged).
    dodged = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        car_x += x_change
        window.fill(white)

        obstacles(obstacle_startx, obstacle_starty, obstacle_width, obstacle_height, block_color)
        obstacle_starty += obstacle_speed
        car(car_x, car_y)

        # TODO: Call the obstacles_dodged function with the correct argument.
        obstacles_dodged(dodged)

        if car_x > display_width - car_width or car_x < 0:
            crash()

        if obstacle_starty > display_height:
            obstacle_starty = 0 - obstacle_height
            obstacle_startx = random.randrange(0, display_width)
            dodged += 1  # Increment the score variable.
            obstacle_speed += 1
            obstacle_width += (dodged * 1.2)

        if car_y < obstacle_starty + obstacle_height:
            if car_x > obstacle_startx and car_x < obstacle_startx + obstacle_width or \
               car_x + car_width > obstacle_startx and car_x + car_width < obstacle_startx + obstacle_width:
                crash()

        pygame.display.update()
        clock.tick(60)

# Main game loop
game_intro()
game_loop()
pygame.quit()
quit()
