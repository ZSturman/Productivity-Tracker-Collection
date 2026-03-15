import pygame
import random
import time


def run_game():
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True
    square_side = 50
    color = (255, 0, 0)  # red
    location = (random.randint(0, screen_width-square_side), 
                random.randint(0, screen_height-square_side))
    start_time = time.time()
    max_squares = 10  # maximum number of squares
    total_playtime = 60  # total playtime in seconds
    score = 0  # score
    miss_penalty = 1  # penalty for misses
    time_penalty_factor = 1  # affects how much reaction time reduces score for a hit

    def draw_square(location):
        pygame.draw.rect(screen, color, pygame.Rect(location[0], location[1], square_side, square_side))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                reaction_time = time.time() - start_time
                if location[0] <= pos[0] <= location[0] + square_side and \
                location[1] <= pos[1] <= location[1] + square_side:
                    print(f"Hit! Reaction time: {reaction_time} seconds")
                    score_increment = max(1, int(time_penalty_factor / reaction_time))  # minimum score increment is 1
                    score += score_increment
                    print(f"Score: {score}")
                    if score >= max_squares:
                        running = False
                        break
                    location = (random.randint(0, screen_width-square_side), 
                                random.randint(0, screen_height-square_side))
                    start_time = time.time()
                else:  # miss
                    score -= miss_penalty
                    print(f"Miss! Score: {score}")
            # end the game after total_playtime seconds
            if time.time() - start_time >= total_playtime:
                running = False
                break

        screen.fill((0, 0, 0))
        draw_square(location)
        pygame.display.flip()

    print(f"Game ended. Total score: {score}")
    pygame.quit()
