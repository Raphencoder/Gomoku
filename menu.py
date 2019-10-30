import pygame
#from visu import vsai
#from visu import vshuman

"""
TODO
    vsai and vshuman functions to replace None l52-53
"""

white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)

def quit_game():
    pygame.quit()
    quit()

def button(x, y, w, h, msg, window, action=None):
    "button function attached to a an action(object)"
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

 # if mouse over the button highliht it
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, grey,(x,y,w,h))
        #perform button action
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, black,(x,y,w,h), 1)
    #text of button
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    window.blit(textSurf, textRect)

def game_intro(window):
    """
    start menu with 2 mode for now, 2 human player and human vs Ai"
    """
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Gomoku", largeText)
        TextRect.center = ((800/2),(800/2))
        window.blit(TextSurf, TextRect)

        button(300,500,200,50, "2 players", window, None)
        button(300, 600, 200, 50, "player VS AI", window, None)
        button(300, 700, 200, 50, "Exit", window, quit_game)
        pygame.display.update()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
