import sys, pygame
import os
import random

# pygame setup
pygame.init()
size = width, height = (1200, 800)
screen = pygame.display.set_mode(size)
title = pygame.display.set_caption("Food Ninja")

# control frame rate
clock = pygame.time.Clock()
#game duration (in ms)
game_duration = 60000


# fonts
title_font = pygame.font.Font(None, 64)
start_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)
duration_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 24)

#colour scheme
beige = 232, 230, 216
white = 255, 255, 255
grey = 203, 212, 214

# homepage + instructions
game_title = "Fruit Ninja Dupe"
instructions_title = "How to Play"
objective = "Objective: Create as many fruit salads as you can. The number of times you can create a complete version of the fruit salad will be your final score."
rule_one = "1. The ingredients required for the fruit salad will be displayed at the top of the screen. Click on the correct fruits as they move across the screen."
rule_two = "2. Each time you click on the wrong ingredient, your final score will be deducted by 1."
rule_three = "3. Press the Enter key to start the game!"
instructions = [instructions_title, objective, rule_one, rule_two, rule_three]
height_shift = 30
all_fruits = ["apple", "banana", "blueberry", "cherry", "coconut", "grape", "lemon", "mango", "orange", "peach", "pear", "pineapple", "strawberry"]

# timer 
timer_x = width/10
timer_y = height/40

# deductions counter
deductions_x = width - width/10
deductions_y = height/40

# fruit counter dashboard 
score = "0"
deductions = "0"
dashboard_height = height/12
fruit_display_width = width/4
fruit_shift = width/4
score_alignment = 50


# game variables
left_margin = 10
right_margin = 10

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
    def __init__(self, fruits, number):
        self.all_fruits = fruits
        # list to randomize in random_fruits method
        self.randomize_fruits = fruits
        self.number = number

        # start game timer - time since pygame.init started
        self.start_time = pygame.time.get_ticks()
        self.last_creation_time = self.start_time

        # randomnly select fruits that player needs to collect
        self.selected_fruits = self.random_fruits()

        #load images of randomnly selected fruits
        self.random_images = self.load_images()

        # create list of falling fruits
        self.falling_fruits = []
        # create fruits
        self.fruit_creation()

    def random_fruits(self):
        '''randomnly select a chosen number of fruits for each game and store in a list'''
        fruit_combo = []
        for i in range(self.number):
            selected_fruit = random.choice(self.randomize_fruits)
            # update randomize_fruits list to not include the selected fruit to prevent repeats
            # updated list will only include fruits not yet selected
            self.randomize_fruits = [fruit for fruit in self.randomize_fruits if fruit != selected_fruit]
            fruit_combo.append(selected_fruit)
        return fruit_combo

    def load_images(self):
        ''' load images of selected fruits '''
        images = {}
        # load + scale images of randomnly selected fruits
        for fruit in (self.selected_fruits):
            img = pygame.image.load(os.path.join("images",f"{fruit}.png")).convert_alpha()
            #scale imgs the same size and store in dictionary
            images[fruit] = pygame.transform.scale(img, (50, 50))
        return images

    def game_timer(self):
        '''game is 60 seconds, calculate remaining time in ms'''
        #get current time since pygame.init started
        current_time = pygame.time.get_ticks() 
        # determine current duration by finding how much time has passed since the player instance was created
        current_duration = current_time - self.start_time

        #display countdown
        remaining_time = game_duration - current_duration
        return remaining_time

    def dashboard(self, score, deductions):
        '''dashboard to count randomnly selected fruits, display timer, and show deductions'''

        #blit countdown - convert to seconds
        time_sec = round(self.game_timer()/1000, 1)
        countdown_img = score_font.render(f"Time Left: {str(time_sec)}", True, (0, 0, 0))
        countdown_rect = countdown_img.get_rect(center = (timer_x, timer_y))
        screen.blit(countdown_img, countdown_rect) 

        # blit deductions
        deductions_img = score_font.render(f"Deductions: {deductions}", True, (0, 0, 0))
        deductions_rect = deductions_img.get_rect(center = (deductions_x, deductions_y))
        screen.blit(deductions_img, deductions_rect)

        # blit fruit counter
        for i, fruit_img in enumerate(self.random_images.values()):
            # blit fruit
            fruit_rect = fruit_img.get_rect(center = (fruit_display_width + (fruit_shift * i), dashboard_height))
            screen.blit(fruit_img, fruit_rect)

            # blit score
            score_img = score_font.render(score, True, (0,0,0))
            score_rect = score_img.get_rect(center=(fruit_display_width + (fruit_shift * i) + score_alignment, dashboard_height))
            screen.blit(score_img, score_rect)

    def fruit_creation(self):
        '''create a random number of fruit instances and stores instances in a list'''
        # random number of fruits that will fall at once
        num_fruits = random.randint(1, 8)

        # create fruit instances from fallingFruit class 
        for i in range(num_fruits):
            # add fruit to falling_fruits list
            self.falling_fruits.append(fallingFruit(self.all_fruits))

    def creation_frequency(self):
        ''' control frequency at which new fruits are created '''
        # timer counting up in ms 
        timer = pygame.time.get_ticks() - self.start_time
        
        # frequency at which new fruits should be created in ms
        if timer < game_duration * 0.25:
            interval = 4000
        elif timer < game_duration * 0.5:
            interval = 3000
        elif timer < game_duration * 0.75:
            interval = 2000
        else:
            interval = 1000
        
        # check if new fruits need to be created
        if timer - self.last_creation_time >= interval:
            self.last_creation_time = timer
            return True
        
        return False

    def fruit_movement(self):
        '''controls movement of current fruits down the screen'''

        # loop through list of fruit instances and update coordinates on screen (i.e. make fruits fall)
        for fruit in self.falling_fruits:
            fruit.update_y()
            fruit.draw_fruit()

            # remove fruit from falling list if outside of screen
            if fruit.x < 0 or fruit.x > width or fruit.y < 0 or fruit.y > height:
                self.falling_fruits.remove(fruit)

    def score(self):
        '''count score'''
        # correct fruit + no increase in completed fruit salads
        # increase score of fruit by 1 and update dashboard

        # correct fruit + increase in completed fruit salads
        # increase score of fruit by 1 and update dashboard + increase total score by 1

        # when player clicks on incorrect fruit
        # increase deductions score by 1 and decrease total score by 1

        pass

class fallingFruit:
    def __init__(self, fruits):
        self.fruits = fruits
        #randomnly select a falling fruit
        self.name = random.choice(fruits)

        # create coordinates and falling speed
        self.x = random.randint(left_margin, width - right_margin)
        # start falling fruits below dashboard
        self.y = dashboard_height * 2
        self.speed = random.randint(1,10)

        # create image of fruit
        self.image = self.load_image()

    def load_image(self):
        ''' load images of selected fruit'''
        # load + scale the image of falling fruit
        img = pygame.image.load(os.path.join("images",f"{self.name}.png")).convert_alpha()
        #scale imgs the same size and store in dictionary
        image = pygame.transform.scale(img, (50, 50))
        return image

    def update_y(self):
        ''' update the y value to allow the fruit to move down screen'''
        self.y += self.speed

    def draw_fruit(self):
        ''' draw fruit on screen '''
        falling_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, falling_rect)


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
                    player = fruitGame(all_fruits, 3)
                    
        # display instructions
        if game_start == False and game_completion == False:
            screen.fill(beige)
            game_instructions(game_title, instructions)

        # start game, 
        if game_start == True:
            # reset screen
            screen.fill(beige)

            # display dashboard
            player.dashboard(score, deductions)

            # move fruits down screen
            player.fruit_movement()

            # check if new fruits need to be created
            create = player.creation_frequency()
            if create == True:
                player.fruit_creation()

            # end game after 60 seconds
            if player.game_timer() <= 0:
                pygame.time.delay(1000)
                game_start = False
                game_completion = True

                # display score
                screen.fill(beige)

        # flip() the display to put your work on screen
        pygame.display.flip()
        # runs 60 frames per second
        clock.tick(60)

if __name__ == "__main__":
    main()



