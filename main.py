import random

import numpy as np
import pygame
import sys
from pygame.locals import *
from line_profiler import *

# import random

pygame.init()

FPS = 100
FramePerSec = pygame.time.Clock()
timer = pygame.time.get_ticks()
CellFramePerSec = 30

# Predefined some colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen information
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 4
LINE_THICKNESS = 1

text_font = pygame.font.Font("freesansbold.ttf", 32)
text = text_font.render("SAND", True, GREEN)
text_rect = text.get_rect()

# Display stuff
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

# Variables
base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # base surface to blit everything onto
sprites = []  # all the rects that make up the grid
Cell_Array = np.zeros(shape=(SCREEN_HEIGHT // CELL_SIZE, SCREEN_WIDTH // CELL_SIZE))  # Where all cell will be stored

valid_substance = [
    "sand",
    "solid",
    "empty",
]  # valid substances each cell can be

# Sprite Groups
movable_group = pygame.sprite.Group()  # Group for all movable cells
liquid_group = pygame.sprite.Group()  # Group for all liquid cells
solid_group = pygame.sprite.Group()  # Group for all solid cells
Cell_Type = valid_substance[0]


# Cell class to handle each cell
class Cell(pygame.sprite.Sprite):

    def __init__(self, position, substance="sand"):
        # self.falling = True
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  # set the surface
        self.rect = position  # set the rect to the position
        self.substance = substance
        self.acceleration = 0

        if substance == "sand":
            self.image.fill((194, 178, 128))
            movable_group.add(self)
            Cell_Array[position[1] // CELL_SIZE, position[0] // CELL_SIZE] = 2
        elif substance == "solid":
            self.image.fill((255, 255, 255))
            solid_group.add(self)
            self.falling = False
            Cell_Array[position[1] // CELL_SIZE, position[0] // CELL_SIZE] = 1

    # Moves cell downwards
    @profile
    def fall(self):
        try:
            if Cell_Array[(self.rect[1] + CELL_SIZE) // CELL_SIZE, self.rect[0] // CELL_SIZE] == 0.0:
                # self.acceleration = 1
                if self.substance == "sand":
                    Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 0
                    self.rect = (self.rect[0], self.rect[1] + 1 * CELL_SIZE)
                    Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 2
                    base_surf.blit(self.image, self.rect)
            elif random.choice([0, 1]):
                if Cell_Array[(self.rect[1] + CELL_SIZE) // CELL_SIZE, (self.rect[0] - CELL_SIZE) // CELL_SIZE] == 0.0 and\
                        Cell_Array[self.rect[1] // CELL_SIZE, (self.rect[0] - CELL_SIZE) // CELL_SIZE] == 0.0:
                    Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 0
                    self.rect = (self.rect[0] - CELL_SIZE, self.rect[1] + CELL_SIZE)
                    Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 2
                    base_surf.blit(self.image, self.rect)
            elif Cell_Array[(self.rect[1] + CELL_SIZE) // CELL_SIZE, (self.rect[0] + CELL_SIZE) // CELL_SIZE] == 0.0 and\
                    Cell_Array[self.rect[1] // CELL_SIZE, (self.rect[0] + CELL_SIZE) // CELL_SIZE] == 0.0:
                Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 0
                self.rect = (self.rect[0] + CELL_SIZE, self.rect[1] + CELL_SIZE)
                Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 2
                base_surf.blit(self.image, self.rect)
        except:
            Cell_Array[self.rect[1] // CELL_SIZE, self.rect[0] // CELL_SIZE] = 0
            movable_group.remove(self)


# Draws the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            sprites.append(pygame.draw.rect(base_surf, (150, 150, 150), rect, LINE_THICKNESS))



# game loop
while True:
    # event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # if the user presses LMB to place a cell
        if pygame.mouse.get_pressed()[0]:
            # check if we should delete the cell
            if Cell_Type == "empty":
                x, y = pygame.mouse.get_pos()
                # loop though all sprites
                for i in (solid_group.sprites() + movable_group.sprites() + liquid_group.sprites()):
                    # check if mouse is over the sprite
                    if i.rect == (x // CELL_SIZE * CELL_SIZE, y // CELL_SIZE * CELL_SIZE):
                        # delete it
                        if i in solid_group:
                            Cell_Array[y // CELL_SIZE, x // CELL_SIZE] = 0
                            solid_group.remove(i)
                        if i in movable_group:
                            Cell_Array[y // CELL_SIZE, x // CELL_SIZE] = 0
                            movable_group.remove(i)
                        if i in liquid_group:
                            Cell_Array[y // CELL_SIZE, x // CELL_SIZE] = 0
                            liquid_group.remove(i)
            else:
                x, y = pygame.mouse.get_pos()
                if 0 < x < SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
                    # print(x // CELL_SIZE * CELL_SIZE // CELL_SIZE, x // CELL_SIZE)
                    if Cell_Array[y // CELL_SIZE, x // CELL_SIZE] == 0:
                        Cell((x // CELL_SIZE * CELL_SIZE, y // CELL_SIZE * CELL_SIZE), Cell_Type)

        # check if we should swap the type
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                # swap it
                Cell_Type = valid_substance[valid_substance.index(Cell_Type) - 1]
                text = text_font.render(Cell_Type.upper(), True, GREEN)

    # cell logic for movable solids
    if pygame.time.get_ticks() - timer > CellFramePerSec:

        for movable in movable_group.sprites()[::-1]:
            movable.fall()
        timer = pygame.time.get_ticks()
    # fmt: on
    base_surf.fill((0, 0, 0, 0))  # clears the screen for the next frame
    movable_group.draw(base_surf)  # draws the movable_group
    solid_group.draw(base_surf)  # draws the movable_group
    # movable_group.draw(base_surf)  # draws the movable_group

    # draws the grid
    # draw_grid()

    base_surf.blit(text, text_rect)
    # displays the base_surf
    DISPLAYSURF.blit(base_surf, (0, 0))
    pygame.display.flip()
    FramePerSec.tick(FPS)
