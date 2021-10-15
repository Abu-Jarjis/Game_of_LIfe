import numpy as np
import pygame as pg
import math
import sys
import random

np.set_printoptions(threshold=sys.maxsize)
#------------------------------
RADIUS = 4
X_LENGTH = math.ceil(1200/(RADIUS*2)) 
Y_LENGTH = math.ceil(1000/(RADIUS*2))
clock = pg.time.Clock()
class Board:
    def __init__(self, grid_height, grid_width, grid, screen) -> None:
        self.grid = grid
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.screen = screen
        self.color = (0,0,0)

    def add_Grid(self):
        for n1,i in enumerate(range(0, self.grid_width ,RADIUS*2)):
            for n2,j in enumerate(range(0, self.grid_height, RADIUS*2)):
                self.grid[n1,n2] = (i,j)
    def draw_Grid(self):
        for i in range(X_LENGTH):
            for j in range(Y_LENGTH):
                pg.draw.circle(self.screen, (0,0,0), self.grid[i,j], RADIUS, width=1)

class Game(Board):
    def __init__(self, grid_height, grid_width, temp, grid, next_gen, screen) -> None:
        super().__init__(grid_height, grid_width, grid, screen)
        self.temp = temp
        self.next_gen = next_gen
    
    def random_game(self):
        for i in range(X_LENGTH):
            for j in range(Y_LENGTH):
                self.temp[i,j] = random.randint(0,1)
    def evolve_cell(self, alive, neighbours):
        return neighbours == 3 or (alive and neighbours == 2)

    def draw_cell(self):
        for i in range(X_LENGTH):
            for j in range(Y_LENGTH):
                if self.next_gen[i,j] == 1:
                    pg.draw.circle(self.screen, [random.randrange(100,255) for _ in range(3)], self.grid[i,j], RADIUS)
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
        for i in range(X_LENGTH):
            for j in range(Y_LENGTH):
                    neighbour = self.check_alive(i,j)
                    if not self.temp[i,j] and neighbour == 3:
                        self.next_gen[i,j] = 1
                    elif self.temp[i,j] and neighbour in (2,3):
                        self.next_gen[i,j] =1
                    else:
                        pass
                        
                    
                    #print(new_grid[i,j])
        self.temp[:,:] = self.next_gen[:,:] 
    
        self.draw_cell()

def main():

    #Screen
    height = 1000
    width = 1200
    screen = pg.display.set_mode((width, height))
    color = (0,0,0)

    #Grid data
    grid_width = width
    grid_height = height
    grid = np.zeros((X_LENGTH,Y_LENGTH), dtype = tuple)
    temp = np.zeros((X_LENGTH,Y_LENGTH), dtype = int)
    next_gen = np.zeros((X_LENGTH,Y_LENGTH), dtype = int)


    game = Game(grid_height, grid_width, temp, grid, next_gen, screen)
    game.add_Grid()
    game.random_game()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(color)
        game.draw_Grid()
        game.Evolve()
            
        clock.tick(20)
        pg.display.update()
