import sys, pygame
import os
import random
from constants import SIZE, WIDTH, HEIGHT, GAME_DURATION, GAME_LEFT_MARGIN, GAME_RIGHT_MARGIN, BEIGE, ALL_FRUITS
from dashboard import TIMER_X, TIMER_Y, SCORE, DEDUCTIONS_X, DEDUCTIONS_Y, DEDUCTIONS, FRUIT_DASHBOARD_HEIGHT, FRUIT_SCORE_ALIGNMENT, FRUIT_SHIFT, FRUIT_WIDTH
from instructions import GAME_TITLE, INSTRUCTIONS_HEIGHT_SHIFT, INSTRUCTIONS, game_instructions
from game import FruitGame
from fruit import FallingFruit

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE)
title = pygame.display.set_caption("Fruit Salad")
clock = pygame.time.Clock()

# part of screen game occurs
GAME_AREA = pygame.Rect(0, FRUIT_DASHBOARD_HEIGHT * 1.5, WIDTH, HEIGHT - FRUIT_DASHBOARD_HEIGHT * 1.5)

# fonts
TITLE_FONT = pygame.font.Font(None, 64)
START_FONT = pygame.font.Font(None, 36)
SCORE_FONT = pygame.font.Font(None, 36)
FINAL_SCORE_FONT = pygame.font.Font(None, 64)
PARAGRAPH_FONT = pygame.font.Font(None, 24)

# load all fruit images
FRUIT_IMAGES = {}
for fruit in ALL_FRUITS:
    img = pygame.image.load(os.path.join("images", f"{fruit}.png")).convert_alpha()
    FRUIT_IMAGES[fruit] = pygame.transform.scale(img, (50, 50))

# Game Loop
def main():
    run = True
    # users can view instructions before game
    game_start = False
    # game completion status - if true show final score
    game_completion = False

    while run:
        # User clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # start game when user presses enter
                if event.key == pygame.K_RETURN and game_start == False:
                    game_start = True
                    player = FruitGame(ALL_FRUITS, FRUIT_IMAGES, 3)
            if game_start:
                player.score(event)
                    
        # display instructions
        if game_start == False and game_completion == False:
            screen.fill(BEIGE)
            game_instructions(GAME_TITLE, INSTRUCTIONS, screen, TITLE_FONT, PARAGRAPH_FONT)

        # start game, 
        if game_start == True and game_completion == False:
            # reset screen
            screen.fill(BEIGE)

            # display dashboard
            player.dashboard(screen, SCORE_FONT)

            # move fruits down screen
            player.fruit_movement(screen)

            # check if new fruits need to be created
            create = player.creation_frequency()
            if create == True:
                player.fruit_creation()

            # end game after 60 seconds
            if player.game_timer() <= 0:
                pygame.time.delay(1000)
                game_completion = True

                # display score
                screen.fill(BEIGE, GAME_AREA)
                total_score_img = FINAL_SCORE_FONT.render(f"Final Score: {str(player.total_score)}", True, (0,0,0))
                total_rect = total_score_img.get_rect(center=(WIDTH/2, HEIGHT/2))
                screen.blit(total_score_img, total_rect)

        # flip() the display to put your work on screen
        pygame.display.flip()
        # runs 60 frames per second
        clock.tick(60)

if __name__ == "__main__":
    main()



