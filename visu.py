import pygame
import os
import sys 

window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("gomoku")
fps = pygame.time.Clock()
score = 0

def game_over():
    os.system('clear')
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
            pass
    window.fill(pygame.Color(243, 210, 132))
    pygame.draw.rect(window, (0, 0, 0), (30, 30, 730, 730), 2)
    L = 700
    nb_square = range(14)
    size_square = int(L / 14) + 6
    square = range(size_square)
    for i in nb_square:
        cube_pos = size_square * i
        pygame.draw.line(window, (0, 0, 0), (30, 30 + cube_pos), (730 + 30, 30 + cube_pos), 1) # largeur
        pygame.draw.line(window, (0, 0, 0), (30 + cube_pos, 30), (30 + cube_pos, 730 + 30), 1) # longueur
    pi = 0
    large = 0
    for i in range(196):
        pi  += 86
        large = 0
        for l in range(14):
            large += 56
            pygame.draw.line(window, (0, 0, 0), (large, pi), (large, pi + 10), 3)
    pygame.display.flip()
