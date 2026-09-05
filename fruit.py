import random
from constants import GAME_LEFT_MARGIN, GAME_RIGHT_MARGIN, WIDTH
from dashboard import FRUIT_DASHBOARD_HEIGHT

class FallingFruit:
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

    def draw(self, screen):
        ''' draw fruit on screen '''
        falling_rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, falling_rect)