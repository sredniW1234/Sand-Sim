import numpy as np
import pygame
import sys
from pygame.locals import *
import cProfile

# import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
timer = pygame.time.get_ticks()
CellFramePerSec = 20

# Predefined some colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen information
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 20
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
            Cell_Array[position[1] // CELL_SIZE][position[0] // CELL_SIZE] = 2
        elif substance == "solid":
            self.image.fill((255, 255, 255))
            solid_group.add(self)
            self.falling = False
            Cell_Array[position[1] // CELL_SIZE][position[0] // CELL_SIZE] = 1

    # Moves cell downwards
    def fall(self):
        try:
            if Cell_Array[(movable.rect[1] + CELL_SIZE) // CELL_SIZE][movable.rect[0] // CELL_SIZE] == 0.0:
                movable.acceleration = 1
            match self.substance:
                case "sand":
                    Cell_Array[self.rect[1] // CELL_SIZE][self.rect[0] // CELL_SIZE] = 0
                    self.rect = (self.rect[0], self.rect[1] + self.acceleration * 20)
                    Cell_Array[self.rect[1] // CELL_SIZE][self.rect[0] // CELL_SIZE] = 2
                    draw_onto_screen("movable")
        except:
            movable_group.remove(self)


# Draws the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            sprites.append(pygame.draw.rect(base_surf, (150, 150, 150), rect, LINE_THICKNESS))


def draw_onto_screen(cell_type):
    match cell_type:
        case "movable":
            movable_group.update()  # updates the movable_group
            movable_group.draw(base_surf)  # draws the movable_group
        case "solid":
            solid_group.update()  # updates the solid_group
            solid_group.draw(base_surf)  # draws the solid_group
        case "liquid":
            liquid_group.update()  # updates the liquid_groud
            liquid_group.draw(base_surf)  # draws the liquid_group

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
                    if i.position == (x // CELL_SIZE * CELL_SIZE, y // CELL_SIZE * CELL_SIZE):
                        # delete it
                        if i in solid_group:
                            solid_group.remove(i)
                        if i in movable_group:
                            movable_group.remove(i)
                        if i in liquid_group:
                            liquid_group.remove(i)
            else:
                x, y = pygame.mouse.get_pos()
                if 0 < x < SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
                    cell = Cell((x // CELL_SIZE * CELL_SIZE, y // CELL_SIZE * CELL_SIZE), Cell_Type)

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
            # try:
            # fmt: off

            # Checks for solid underneath
            #   if base_surf.get_at((
            #       movable.position[0] + 2 * LINE_THICKNESS,
            #       movable.position[1] + CELL_SIZE + CELL_SIZE // 2,
            #   )) in [(255, 255, 255), (194, 178, 128)]:
            #     # checks if the sand can fall to the left
            #     if base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS - CELL_SIZE, movable.position[1] + CELL_SIZE + CELL_SIZE // 2)) != (255, 255, 255) and \
            #         base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS - CELL_SIZE, movable.position[1] + CELL_SIZE + CELL_SIZE // 2)) != (194, 178, 128) and \
            #         not movable.falling and base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS + CELL_SIZE, movable.position[1] + 2 * LINE_THICKNESS)) != (255, 255, 255)\
            #             and base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS - CELL_SIZE, movable.position[1] + 2 * LINE_THICKNESS)) != (255, 255, 255):
            #       # set the position to down 1 and left 1
            #       movable.position = (movable.position[0] - CELL_SIZE,
            #                           movable.position[1])
            #       movable.acceleration = 1
            #       movable.fall()
            #
            #     # checks if the sand can fall to the right
            #     elif base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS + CELL_SIZE, movable.position[1] + CELL_SIZE + CELL_SIZE // 2)) != (255, 255, 255) and \
            #         base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS + CELL_SIZE, movable.position[1] + CELL_SIZE + CELL_SIZE // 2)) != (194, 178, 128) and \
            #         not movable.falling and base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS + CELL_SIZE, movable.position[1] + 2 * LINE_THICKNESS)) != (255, 255, 255)\
            #             and base_surf.get_at((movable.position[0] + 2 * LINE_THICKNESS - CELL_SIZE, movable.position[1] + 2 * LINE_THICKNESS)) != (255, 255, 255):
            #       # set the position to down 1 and right 1
            #       movable.position = (movable.position[0] + CELL_SIZE,
            #                           movable.position[1])
            #       movable.acceleration = 1
            #       movable.fall()
            #     else:
            #       movable.falling = False
            #
            #
            #   else:
            #     movable.acceleration = 1
            #     movable.fall()
            # except IndexError:
            #   movable_group.remove(movable)
        timer = pygame.time.get_ticks()
    # fmt: on
    base_surf.fill((0, 0, 0, 0))  # clears the screen for the next frame
    draw_onto_screen("movable")
    draw_onto_screen("solid")

    # draws the grid
    draw_grid()

    base_surf.blit(text, text_rect)
    # displays the base_surf
    DISPLAYSURF.blit(base_surf, (0, 0))
    pygame.display.flip()
    FramePerSec.tick(FPS)
