import numpy as np
from numpy.lib.utils import safe_eval
import pygame as pg
import math
import sys
import random

from pygame.display import set_caption

np.set_printoptions(threshold=sys.maxsize)
clock = pg.time.Clock()
pg.display.set_caption("Game of Life")
#------------------------------
STATE = 1
RADIUS = 4
X_LENGTH = math.ceil(1200/(RADIUS*2)) 
Y_LENGTH = math.ceil(1000/(RADIUS*2))
class Board:
    def __init__(self, grid_height, grid_width, grid, screen) -> None:
        self.grid = grid
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.screen = screen
        self.color = (0,0,100)

    def add_Grid(self):
        for n1,i in enumerate(range(0, self.grid_height ,RADIUS*2)):
            for n2,j in enumerate(range(0, self.grid_width, RADIUS*2)):
                self.grid[n1,n2] = (j,i)

    def draw_Grid(self):
        for i in range(Y_LENGTH):
            for j in range(X_LENGTH):
                pg.draw.circle(self.screen, self.color, self.grid[i,j], RADIUS, width=1)

class Game(Board):
    def __init__(self, grid_height, grid_width, temp, grid, next_gen, screen, state) -> None:
        super().__init__(grid_height, grid_width, grid, screen)
        self.temp = temp
        self.next_gen = next_gen
        self.state = state
        self.color_cell = (0,120,240)
    def random_game(self):
        for i in range(Y_LENGTH):
            for j in range(X_LENGTH):
                self.temp[i,j] = random.randint(0,1)
    def evolve_cell(self, alive, neighbours):
        return neighbours == 3 or (alive and neighbours == 2)

    def draw_cell(self):
        for i in range(Y_LENGTH):
            for j in range(X_LENGTH):
                if self.next_gen[i,j] == 1:
                    pg.draw.circle(self.screen, self.color_cell, self.grid[i,j], RADIUS)
        #RULE #4: ALL OTHER LIVING CELLS DIE
        self.next_gen[self.next_gen > 0] = 0 
                

    def check_alive(self, i, j):
            count = 0
            if_alive = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1) 
                    , (i, j+1), (i+1, j-1), (i+1, j), (i+1,j+1)
                    ]
            try:
                neightbour_count = len([self.temp[i,j] for i,j in if_alive if self.temp[i,j]])
                return neightbour_count
            except:IndexError

    def Evolve(self):
        for i in range(Y_LENGTH):
            for j in range(X_LENGTH):
                    neighbour = self.check_alive(i,j)
                    if not self.temp[i,j] and neighbour == 3:
                        self.next_gen[i,j] = 1
                    elif self.temp[i,j] and neighbour in (2,3):
                        self.next_gen[i,j] =1
                    else:
                        pass
                        
        self.temp[:,:] = self.next_gen[:,:] 
        self.draw_cell()
    
    def event_handler(self, event, keys):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.state:
                    self.state = 0
                else:
                    self.state = 1
            if event.key == pg.K_r:
                self.temp[:, :] = 0

        if keys[pg.K_c]:
            try:
                for i in range(Y_LENGTH):
                    temp_grid = self.grid[i,:]
                    within_cell = [(x,y) for y, x in enumerate(temp_grid) if math.dist(x, pg.mouse.get_pos()) < RADIUS]
                    if within_cell:
                        break
                self.temp[i,within_cell[0][1]] = 1
                pg.draw.circle(self.screen, self.color_cell, within_cell[0][0], RADIUS)
            except IndexError: pass
 

def Game_of_Life():

    #Screen
    height = 1000
    width = 1200
    screen = pg.display.set_mode((width, height))
    color = (0,0,0)

    #Grid data
    grid_width = width
    grid_height = height
    grid = np.zeros((Y_LENGTH,X_LENGTH), dtype = tuple)
    temp = np.zeros((Y_LENGTH,X_LENGTH), dtype = int)
    next_gen = np.zeros((Y_LENGTH,X_LENGTH), dtype = int)


    game = Game(grid_height, grid_width, temp, grid, next_gen, screen, state=1)
    game.add_Grid()
    #game.random_game()
    #game.temp[:, 0:X_LENGTH//2:3] = 1
    
    

    while True:
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            game.event_handler(event, keys)
        if game.state == 1:
            
            screen.fill(color)
            game.draw_Grid()
            game.Evolve()
            pg.display.update()
        else:
            pg.display.update()
        clock.tick(30)

