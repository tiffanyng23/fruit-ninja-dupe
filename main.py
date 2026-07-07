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
final_score_font = pygame.font.Font(None, 64)
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

# fruits used in game
all_fruits = ["apple", "banana", "blueberry", "cherry", "coconut", "grape", "lemon", "mango", "orange", "peach", "pear", "pineapple", "strawberry"]
# load fruit images
fruit_images = {}
for fruit in all_fruits:
    img = pygame.image.load(os.path.join("images", f"{fruit}.png")).convert_alpha()
    fruit_images[fruit] = pygame.transform.scale(img, (50, 50))


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
game_area = pygame.Rect(0, dashboard_height * 1.5, width, height - dashboard_height * 1.5)
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
    def __init__(self, fruits, fruit_images, number):
        self.all_fruits = fruits
        self.fruit_images = fruit_images
        # list to randomize in random_fruits method
        self.randomize_fruits = fruits
        self.number = number

        # start game timer - time since pygame.init started
        self.start_time = pygame.time.get_ticks()
        self.last_creation_time = self.start_time

        # randomnly select fruits that player needs to collect
        self.fruit_salad = self.random_fruits()

        #extract images of chosen fruits to display on dashboard
        self.dashboard_images = {}
        for correct_fruit in self.fruit_salad:
            self.dashboard_images[correct_fruit] = self.fruit_images[correct_fruit]

        # create first batch of fruits
        self.falling_fruits = []
        self.fruit_creation()

        # game scores
        self.fruit_scores = {}
        for fruit in self.fruit_salad:
            self.fruit_scores[fruit] = 0

        self.deductions = 0
        self.total_score = 0

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

    def game_timer(self):
        '''game is 60 seconds, calculate remaining time in ms'''
        #get current time since pygame.init started
        current_time = pygame.time.get_ticks() 
        # determine current duration by finding how much time has passed since the player instance was created
        current_duration = current_time - self.start_time

        #display countdown
        remaining_time = game_duration - current_duration
        return remaining_time

    def dashboard(self):
        '''dashboard to count randomnly selected fruits, display timer, and show deductions'''

        #blit countdown - convert to seconds
        time_sec = round(self.game_timer()/1000, 1)
        countdown_img = score_font.render(f"Time Left: {str(time_sec)}", True, (0, 0, 0))
        countdown_rect = countdown_img.get_rect(center = (timer_x, timer_y))
        screen.blit(countdown_img, countdown_rect) 

        # blit deductions
        deductions_img = score_font.render(f"Deductions: {self.deductions}", True, (0, 0, 0))
        deductions_rect = deductions_img.get_rect(center = (deductions_x, deductions_y))
        screen.blit(deductions_img, deductions_rect)

        # blit fruit dashboard
        for i, (fruit_name, fruit_img) in enumerate(self.dashboard_images.items()):
            # blit fruit
            fruit_rect = fruit_img.get_rect(center = (fruit_display_width + (fruit_shift * i), dashboard_height))
            screen.blit(fruit_img, fruit_rect)

            # blit score
            # extract score
            score = str(self.fruit_scores[fruit_name])
            score_img = score_font.render(score, True, (0,0,0))
            score_rect = score_img.get_rect(center=(fruit_display_width + (fruit_shift * i) + score_alignment, dashboard_height))
            screen.blit(score_img, score_rect)

    def fruit_creation(self):
        '''create a random number of fruit instances and stores instances in a list'''
        # random number of fruits that need to be created and will fall at once
        num_fruits = random.randint(1, 8)

        # create fruit instances from fallingFruit class 
        for i in range(num_fruits):
            # add each fruit to falling_fruits list
            self.falling_fruits.append(fallingFruit(self.all_fruits, fruit_images))

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
        for fruit in self.falling_fruits[:]:
            fruit.update_y()
            fruit.draw_fruit()

            # remove fruit from falling list if outside of screen
            if fruit.x < 0 or fruit.x > width or fruit.y < 0 or fruit.y > height:
                self.falling_fruits.remove(fruit)

    def score(self, event):
        '''record and count score'''

        # check if player clicked a fruit
        if event.type == pygame.MOUSEBUTTONDOWN:
            for falling_fruit in self.falling_fruits[:]:
                # get rect of the falling fruit
                rect = falling_fruit.image.get_rect(center=(falling_fruit.x, falling_fruit.y))
                
                # check if click occured within coordinates of one of the falling fruits
                if rect.collidepoint(event.pos):
                    # if yes, check if fruit is one of the correct fruits to click
                    correct_fruit = False
                    for fruit in self.fruit_salad:
                        if fruit == falling_fruit.name:
                            # increase score by 1
                            self.fruit_scores[fruit] += 1
                            print(f"{fruit} +1")

                            # remove fruit instance from falling fruits instance list if correct
                            self.falling_fruits.remove(falling_fruit)
                            correct_fruit = True
                            break
                    if not correct_fruit:
                        # fruit not any of the correct fruits, reduce score by 1
                        self.deductions += 1
                        self.total_score -= 1
                        self.falling_fruits.remove(falling_fruit)

                    # update total score
                    fruit_salad_score = sorted(list(self.fruit_scores.values()))[0]
                    self.total_score = fruit_salad_score - self.deductions
                    print(f"total score: {self.total_score}")


class fallingFruit:
    def __init__(self, fruits, fruit_images):
        self.fruits = fruits
        #randomnly select one falling fruit and store its name
        self.name = random.choice(fruits)

        # store image of the falling fruit
        self.image = fruit_images[self.name]

        # create starting coordinates
        self.x = random.randint(left_margin, width - right_margin)
        # start falling fruits below dashboard
        self.y = dashboard_height * 2
        self.speed = random.randint(1,10)

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
                    player = fruitGame(all_fruits, fruit_images, 3)
            if game_start:
                player.score(event)
                    
        # display instructions
        if game_start == False and game_completion == False:
            screen.fill(beige)
            game_instructions(game_title, instructions)

        # start game, 
        if game_start == True:
            # reset screen
            screen.fill(beige)

            # display dashboard
            player.dashboard()

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
                screen.fill(beige, game_area)
                total_score_img = final_score_font.render(f"Final Score {str(player.total_score)}", True, (0,0,0))
                total_rect = total_score_img.get_rect(center=(width/2, height/2))
                screen.blit(total_score_img, total_rect)

        # flip() the display to put your work on screen
        pygame.display.flip()
        # runs 60 frames per second
        clock.tick(60)

if __name__ == "__main__":
    main()



