from constants import WIDTH, HEIGHT

GAME_TITLE = "Fruit Salad"
instructions_title = "How to Play"
objective = "Objective: Create as many fruit salads as you can. The number of times you can create a complete version of the fruit salad will be your final score."
rule_one = "1. The ingredients required for the fruit salad will be displayed at the top of the screen. Click on the correct fruits as they move across the screen."
rule_two = "2. Each time you click on the wrong ingredient, your final score will be deducted by 1."
rule_three = "3. Press the Enter key to start the game!"
INSTRUCTIONS = [instructions_title, objective, rule_one, rule_two, rule_three]
INSTRUCTIONS_HEIGHT_SHIFT = 30

def game_instructions(title, instructions, screen, title_font, paragraph_font):
    '''game instructions'''
    title_img = title_font.render(GAME_TITLE, True, (0,0,0))
    title_rect = title_img.get_rect(center=(WIDTH/2, HEIGHT/4))
    screen.blit(title_img, title_rect)

    for i in range(len(instructions)):
        rules_img = paragraph_font.render(instructions[i], True, (0,0,0))
        # get coordinates at which you want to display the rules
        # shift coordinates for each step 
        rules_rect = rules_img.get_rect(center=(WIDTH/2, (HEIGHT/3 + INSTRUCTIONS_HEIGHT_SHIFT * i)))
        screen.blit(rules_img, rules_rect)