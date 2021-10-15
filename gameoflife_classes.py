import numpy as np
import pygame as pg
import math
import sys
import random
np.set_printoptions(threshold=sys.maxsize)
#------------------------------
clock = pg.time.Clock()
class Board:
    def __init__(self, grid_height, grid_width, temp, grid, next_gen) -> None:
        self.grid = grid
        self.temp = temp
        self.next_gen = next_gen
        self.grid_height = grid_height
        self.grid_width = grid_width

    def add_Grid(self):
        for n1,i in enumerate(range(0, grid_width ,RADIUS*2)):
            for n2,j in enumerate(range(0, grid_height, RADIUS*2)):
                self.grid[n1,n2] = (i,j)
    def draw_Grid(self):
        for i in range(K1):
            for j in range(K2):
                pg.draw.circle(SCREEN, (0,0,0), self.grid[i,j], RADIUS, width=1)

class Game(Board):
    def __init__(self) -> None:
        super().__init__(grid_height, grid_width, temp, grid, next_gen)
    
    def random_game(self):
        for i in range(K1):
            for j in range(K2):
                self.temp[i,j] = random.randint(0,1)
    def evolve_cell(self, alive, neighbours):
        return neighbours == 3 or (alive and neighbours == 2)

    def draw_cell(self):
        for i in range(K1):
            for j in range(K2):
                if self.next_gen[i,j] == 1:
                    pg.draw.circle(SCREEN, (0, 120, 240), self.grid[i,j], RADIUS)
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
        for i in range(K1):
            for j in range(K2):
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
        

            






            



#Screen
height = 1000
width = 1200
color = (0,0,0)
SCREEN = pg.display.set_mode((width, height))

#Grid data
RADIUS = 4
K1 = math.ceil(width/(RADIUS*2)) 
K2 = math.ceil(height/(RADIUS*2))
grid_width = width
grid_height = height
grid = np.zeros((K1,K2), dtype = tuple)
temp = np.zeros((K1,K2), dtype = int)
next_gen = np.zeros((K1,K2), dtype = int)


game = Game()
game.add_Grid()
game.random_game()








def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        SCREEN.fill(color)
        game.draw_Grid()
        game.Evolve()
        #game.draw_cell(self.temp)


        clock.tick(30)
        pg.display.update()
        
