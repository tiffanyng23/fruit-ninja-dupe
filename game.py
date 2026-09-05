import pygame
import random
from fruit import FallingFruit
from constants import SIZE, WIDTH, HEIGHT, GAME_DURATION, GAME_LEFT_MARGIN, GAME_RIGHT_MARGIN, BEIGE, ALL_FRUITS
from dashboard import TIMER_X, TIMER_Y, SCORE, DEDUCTIONS_X, DEDUCTIONS_Y, DEDUCTIONS, FRUIT_DASHBOARD_HEIGHT, FRUIT_SCORE_ALIGNMENT, FRUIT_SHIFT, FRUIT_WIDTH

class FruitGame:
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

    def dashboard(self, screen, score_font):
        '''dashboard to count randomnly selected fruits, display timer, and show deductions'''

        #blit countdown - convert to seconds
        time_sec = round(self.game_timer()/1000, 1)
        countdown_img = score_font.render(f"Time Left: {str(time_sec)}", True, (0, 0, 0))
        countdown_rect = countdown_img.get_rect(center = (TIMER_X, TIMER_Y))
        screen.blit(countdown_img, countdown_rect) 

        # blit deductions
        deductions_img = score_font.render(f"Deductions: {self.deductions}", True, (0, 0, 0))
        deductions_rect = deductions_img.get_rect(center = (DEDUCTIONS_X, DEDUCTIONS_Y))
        screen.blit(deductions_img, deductions_rect)

        # blit fruit dashboard
        for i, (fruit_name, fruit_img) in enumerate(self.dashboard_images.items()):
            # blit fruit
            fruit_rect = fruit_img.get_rect(center = (FRUIT_WIDTH + (FRUIT_SHIFT * i), FRUIT_DASHBOARD_HEIGHT))
            screen.blit(fruit_img, fruit_rect)

            # blit score
            # extract score
            score = str(self.fruit_scores[fruit_name])
            score_img = score_font.render(score, True, (0,0,0))
            score_rect = score_img.get_rect(center=(FRUIT_WIDTH + (FRUIT_SHIFT * i) + FRUIT_SCORE_ALIGNMENT, FRUIT_DASHBOARD_HEIGHT))
            screen.blit(score_img, score_rect)

    def fruit_creation(self):
        '''create a random number of fruit instances and stores instances in a list'''
        # random number of fruits that need to be created and will fall at once
        num_fruits = random.randint(1, 8)

        # create fruit instances from fallingFruit class 
        for i in range(num_fruits):
            # loop num_fruits number of times - each loop generates one random fruit image starting at a random x coordinate
            self.falling_fruits.append(FallingFruit(self.all_fruits, self.fruit_images))

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

    def fruit_movement(self, screen):
        '''controls movement of current fruits down the screen'''

        # loop through list of fruit instances and update coordinates on screen (i.e. make fruits fall)
        for fruit in self.falling_fruits[:]:
            fruit.update_y()
            fruit.draw(screen)

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