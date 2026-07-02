import sys, pygame
import os
import random

# pygame setup
pygame.init()
size = width, height = (1200, 800)
screen = pygame.display.set_mode(size)
title = pygame.display.set_caption("Food Ninja")
clock = pygame.time.Clock()
running = True

# fonts
title_font = pygame.font.Font(None, 64)
start_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 24)

#colour scheme
beige = 232, 230, 216
white = 255, 255, 255
green = 173, 217, 173

# homepage + instructions
game_title = "Fruit Ninja Dupe"
instructions_title = "How to Play"
objective = "Objective: Create as many fruit salads as you can. The number of times you can create a complete version of the fruit salad will be your final score."
rule_one = "1. The ingredients required for the fruit salad will be displayed at the top of the screen. Click on the correct fruits as they fall down the screen."
rule_two = "2. Each time you click on the wrong ingredient, your final score will be deducted by 1."
rule_three = "3. Press the Enter key to start the game!"
instructions = [instructions_title, objective, rule_one, rule_two, rule_three]
height_shift = 30
fruits = ["apple", "banana", "grape", "orange", "peach"]

# fruit counter variables
score = "0"
deductions = "0"
dashboard_height = height/15
fruit_display_width = width/8
fruit_shift = 250
score_alignment = 50
deduction_alignment = 350

# functions
def game_instructions(title, instructions):
    '''game instructions'''
    title_img = title_font.render(game_title, True, (0,0,0))
    title_rect = title_img.get_rect(center=(width/2, height/4))
    screen.blit(title_img, title_rect)

    for i in range(len(instructions)):
        rules_img = font.render(instructions[i], True, (0,0,0))
        # get coordinates at which you want to display the rules
        # shift coordinates for each step 
        rules_rect = rules_img.get_rect(center=(width/2, (height/3 + height_shift * i)))
        screen.blit(rules_img, rules_rect)

    
class fruitGame:
    def __init__(self, name, fruits, number):
        self.name = name
        self.fruits = fruits
        self.number = number

        self.selected_fruits = self.random_fruits()
        self.images = self.load_images()

    def random_fruits(self):
        '''randomnly select a chosen number of fruits for each game'''
        fruit_combo = []
        for i in range(self.number):
            selected_fruit = random.choice(self.fruits)
            # update fruits list to not include the selected fruit to prevent repeats
            self.fruits = [fruit for fruit in self.fruits if fruit != selected_fruit]
            fruit_combo.append(selected_fruit)
        return fruit_combo

    def load_images(self):
        ''' load images of randomnly selected fruits '''
        images = {}
        # load + scale images of randomnly selected fruits
        for fruit in (self.selected_fruits):
            img = pygame.image.load(os.path.join("images",f"{fruit}.png")).convert_alpha()
            #scale imgs the same size and store in dictionary
            images[fruit] = pygame.transform.scale(img, (50, 50))
        return images

    def dashboard(self, score, deductions):
        '''dashboard to count randomnly selected fruits and game score'''
        for i, fruit_img in enumerate(self.images.values()):
            # blit fruit
            fruit_rect = fruit_img.get_rect(center = (fruit_display_width + (fruit_shift * i), dashboard_height))
            screen.blit(fruit_img, fruit_rect)

            # blit score
            score_img = score_font.render(score, True, (0,0,0))
            score_rect = score_img.get_rect(center=(fruit_display_width + (fruit_shift * i) + score_alignment, dashboard_height))
            screen.blit(score_img, score_rect)

            if i == 2:
                # blit deduction count
                deductions_img = score_font.render(f"Deductions: {deductions}", True, (0, 0, 0))
                deductions_rect = deductions_img.get_rect(center = (fruit_display_width + (fruit_shift * i) + deduction_alignment, dashboard_height))
                screen.blit(deductions_img, deductions_rect)

            
    def score(self):
        '''count score'''
        pass

    def falling_fruits(self):
        '''generate randomnly falling fruits'''
        pass

    def timer(self):
        '''game is 60 seconds, countdown display'''
        pass


def main():
    run = True
    # this game_start should begin as false so users can view instructions
    game_start = False
    while run:
        # User clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # start game when user presses enter
                if event.key == pygame.K_RETURN and game_start == False:
                    game_start = True
                    # create player
                    player = fruitGame("player", fruits, 3)

        # display instructions
        if game_start == False:
            screen.fill(beige)
            game_instructions(game_title, instructions)

        # start game
        if game_start == True:
            # reset screen
            screen.fill(beige)
            # load images of randomnly selected fruits
            player.load_images()
            #display fruit counter and score
            player.dashboard(score, deductions)




        # flip() the display to put your work on screen
        pygame.display.flip()

if __name__ == "__main__":
    main()



