import pygame
import random

pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Game variables
moles = []
mole_radius = 30
mole_color = (255, 0, 0)  # red
spawn_time = 1000  # spawn new mole every 1000 milliseconds
last_spawn = pygame.time.get_ticks()
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for mole in moles.copy():
                if ((pos[0] - mole[0])**2 + (pos[1] - mole[1])**2) <= mole_radius**2:
                    moles.remove(mole)
                    score += 1
                    print(f"Mole whacked! Score: {score}")

    if pygame.time.get_ticks() - last_spawn >= spawn_time:
        new_mole = (random.randint(mole_radius, screen_width-mole_radius),
                    random.randint(mole_radius, screen_height-mole_radius))
        moles.append(new_mole)
        last_spawn = pygame.time.get_ticks()

    screen.fill((0, 0, 0))
    for mole in moles:
        pygame.draw.circle(screen, mole_color, mole, mole_radius)
    pygame.display.flip()

pygame.quit()
