import pygame
from component import Ground, Dino,Blockes

win_height= 720
win_width = 550
block_height = 100
window = pygame.display.set_mode((win_width,win_height))
ground = Ground(win_width)
dino = Dino(50, 370)
# Position the dino at x=50, y=370 (so bottom edge is at y=400, on the ground)
block = Blockes(200, 350, 50)  # Much shorter block: height=50, positioned at y=350 so bottom touches ground