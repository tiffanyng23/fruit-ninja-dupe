import sys, pygame
import os
import random

# Variables

# pygame setup
pygame.init()
SIZE = WIDTH, HEIGHT = (1200, 800)
SCREEN = pygame.display.set_mode(SIZE)
TITLE = pygame.display.set_caption("Fruit Salad")
# control frame rate
CLOCK = pygame.time.Clock()
#game duration (in ms)
GAME_DURATION = 60000

# fonts
TITLE_FONT = pygame.font.Font(None, 64)
START_FONT = pygame.font.Font(None, 36)
SCORE_FONT = pygame.font.Font(None, 36)
FINAL_SCORE_FONT = pygame.font.Font(None, 64)
PARAGRAPH_FONT = pygame.font.Font(None, 24)

#colour scheme
BEIGE = 232, 230, 216

# timer display coordinates
TIMER_X = WIDTH/10
TIMER_Y = HEIGHT/40

# deductions counter coordinates
DEDUCTIONS_X = WIDTH - WIDTH/10
DEDUCTIONS_Y = HEIGHT/40

# fruit counter dashboard 
score = "0"
deductions = "0"
FRUIT_DASHBOARD_HEIGHT = HEIGHT/12
FRUIT_WIDTH = WIDTH/4
FRUIT_SHIFT = WIDTH/4
FRUIT_SCORE_ALIGNMENT = 50

# game variables
GAME_AREA = pygame.Rect(0, FRUIT_DASHBOARD_HEIGHT * 1.5, WIDTH, HEIGHT - FRUIT_DASHBOARD_HEIGHT * 1.5)
GAME_LEFT_MARGIN = 10
GAME_RIGHT_MARGIN = 10

# homepage + instructions
GAME_TITLE = "Fruit Salad"
instructions_title = "How to Play"
objective = "Objective: Create as many fruit salads as you can. The number of times you can create a complete version of the fruit salad will be your final score."
rule_one = "1. The ingredients required for the fruit salad will be displayed at the top of the screen. Click on the correct fruits as they move across the screen."
rule_two = "2. Each time you click on the wrong ingredient, your final score will be deducted by 1."
rule_three = "3. Press the Enter key to start the game!"
INSTRUCTIONS = [instructions_title, objective, rule_one, rule_two, rule_three]
INSTRUCTIONS_HEIGHT_SHIFT = 30

# fruits used in game
ALL_FRUITS = ["apple", "banana", "blueberry", "cherry", "coconut", "grape", "lemon", "mango", "orange", "peach", "pear", "pineapple", "strawberry"]
# load all fruit images
FRUIT_IMAGES = {}
for fruit in ALL_FRUITS:
    img = pygame.image.load(os.path.join("images", f"{fruit}.png")).convert_alpha()
    FRUIT_IMAGES[fruit] = pygame.transform.scale(img, (50, 50))


# Functions
def game_instructions(title, instructions):
    '''game instructions'''
    title_img = TITLE_FONT.render(GAME_TITLE, True, (0,0,0))
    title_rect = title_img.get_rect(center=(WIDTH/2, HEIGHT/4))
    SCREEN.blit(title_img, title_rect)

    for i in range(len(instructions)):
        rules_img = PARAGRAPH_FONT.render(instructions[i], True, (0,0,0))
        # get coordinates at which you want to display the rules
        # shift coordinates for each step 
        rules_rect = rules_img.get_rect(center=(WIDTH/2, (HEIGHT/3 + INSTRUCTIONS_HEIGHT_SHIFT * i)))
        SCREEN.blit(rules_img, rules_rect)

# Classes    
class fruitGame:
    def __init__(self, fruits, fruit_images, number):
        self.all_fruits = fruits
        self.fruit_images = fruit_images

        # list to randomize in random_fruits method
        self.randomize_fruits = fruits
        # number of fruits to be selected for the salad
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

        # create first batch of randomized falling fruits
        self.falling_fruits = []
        self.fruit_creation()

        # game score
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
        remaining_time = GAME_DURATION - current_duration
        return remaining_time

    def dashboard(self):
        '''dashboard to count randomnly selected fruits, display timer, and show deductions'''

        #blit countdown - convert to seconds
        time_sec = round(self.game_timer()/1000, 1)
        countdown_img = SCORE_FONT.render(f"Time Left: {str(time_sec)}", True, (0, 0, 0))
        countdown_rect = countdown_img.get_rect(center = (TIMER_X, TIMER_Y))
        SCREEN.blit(countdown_img, countdown_rect) 

        # blit deductions
        deductions_img = SCORE_FONT.render(f"Deductions: {self.deductions}", True, (0, 0, 0))
        deductions_rect = deductions_img.get_rect(center = (DEDUCTIONS_X, DEDUCTIONS_Y))
        SCREEN.blit(deductions_img, deductions_rect)

        # blit fruit dashboard
        for i, (fruit_name, fruit_img) in enumerate(self.dashboard_images.items()):
            # blit fruit
            fruit_rect = fruit_img.get_rect(center = (FRUIT_WIDTH + (FRUIT_SHIFT * i), FRUIT_DASHBOARD_HEIGHT))
            SCREEN.blit(fruit_img, fruit_rect)

            # blit score
            # extract score
            score = str(self.fruit_scores[fruit_name])
            score_img = SCORE_FONT.render(score, True, (0,0,0))
            score_rect = score_img.get_rect(center=(FRUIT_WIDTH + (FRUIT_SHIFT * i) + FRUIT_SCORE_ALIGNMENT, FRUIT_DASHBOARD_HEIGHT))
            SCREEN.blit(score_img, score_rect)

    def fruit_creation(self):
        '''create a random number of fruit instances and stores instances in a list'''
        # random number of fruits that need to be created and will fall at once
        num_fruits = random.randint(1, 8)

        # create fruit instances from fallingFruit class 
        for i in range(num_fruits):
            # loop num_fruits number of times - each loop generates one random fruit image starting at a random x coordinate
            self.falling_fruits.append(fallingFruit(self.all_fruits, FRUIT_IMAGES))

    def creation_frequency(self):
        ''' control frequency at which new fruits are created. Create new fruits if  '''
        # timer counting up in ms 
        timer = pygame.time.get_ticks() - self.start_time
        
        # frequency at which new fruits should be created in ms
        if timer < GAME_DURATION * 0.25:
            interval = 4000
        elif timer < GAME_DURATION * 0.5:
            interval = 3000
        elif timer < GAME_DURATION * 0.75:
            interval = 2000
        else:
            interval = 1000
        
        # check if new fruits need to be created
        if timer - self.last_creation_time >= interval:
            self.last_creation_time = timer
            return True
        
        # no new fruits need to be created yet
        return False

    def fruit_movement(self):
        '''controls movement of current fruits down the screen'''

        # loop through list of fruit instances and update coordinates on screen (i.e. make fruits fall)
        for fruit in self.falling_fruits[:]:
            fruit.update_y()
            fruit.draw_fruit()

            # remove fruit from falling list if outside of screen
            if fruit.x < 0 or fruit.x > WIDTH or fruit.y < 0 or fruit.y > HEIGHT:
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
        #randomnly select one falling fruit out of all the available fruits and store its name
        self.name = random.choice(fruits)

        # extract + store image of the falling fruit
        self.image = fruit_images[self.name]

        # create random starting x coordinate for the fruit
        self.x = random.randint(GAME_LEFT_MARGIN, WIDTH - GAME_RIGHT_MARGIN)
        # start falling fruit at a standard y coordinate 
        self.y = FRUIT_DASHBOARD_HEIGHT * 2
        self.speed = random.randint(1,10)

    def update_y(self):
        ''' update the y value to allow the fruit to move down screen'''
        self.y += self.speed

    def draw_fruit(self):
        ''' draw fruit on screen '''
        falling_rect = self.image.get_rect(center = (self.x, self.y))
        SCREEN.blit(self.image, falling_rect)

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
                    player = fruitGame(ALL_FRUITS, FRUIT_IMAGES, 3)
            if game_start:
                player.score(event)
                    
        # display instructions
        if game_start == False and game_completion == False:
            SCREEN.fill(BEIGE)
            game_instructions(GAME_TITLE, INSTRUCTIONS)

        # start game, 
        if game_start == True and game_completion == False:
            # reset screen
            SCREEN.fill(BEIGE)

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
                game_completion = True

                # display score
                SCREEN.fill(BEIGE, GAME_AREA)
                total_score_img = FINAL_SCORE_FONT.render(f"Final Score: {str(player.total_score)}", True, (0,0,0))
                total_rect = total_score_img.get_rect(center=(WIDTH/2, HEIGHT/2))
                SCREEN.blit(total_score_img, total_rect)

        # flip() the display to put your work on screen
        pygame.display.flip()
        # runs 60 frames per second
        CLOCK.tick(60)

if __name__ == "__main__":
    main()



