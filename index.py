"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states,
alive or dead, or "populated" or "unpopulated". Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent. At each step in time, the following transitions occur:
Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
Outline:
1. Create Board
2. Generate random cells
3. Iterate through rules
"""

import pygame
import random


class Cells:
    def __init__(self, grid):
        self.grid = grid

    # neighbor coordinates
    neighbor_coordinates = {
        (-1,-1),( 0,-1),(1,-1),
        (-1, 0),        (1, 0),
        (-1, 1),( 0, 1),(1, 1)
    }

    # assigns color to a specific cell
    def color_cell(self, color_state, x, y):
        pygame.draw.rect(screen,
                         color_state,
                         [cell_size * y,
                          cell_size * x,
                          cell_size,
                          cell_size])

    # Counts alive-neighbors of chosen cell
    def count_neighbors(self, x, y):
        alive_neighbors = 0
        for i in self.neighbor_coordinates:
            # NeighborX and NeighborY coordinates
            nx = i[0]
            ny = i[1]
            try:
                if self.grid[x + nx][y + ny] == 1:
                    alive_neighbors +=1
            except:
                # Handles errors from cells that are on the edge of the board
                # Error comes from index being out of range (cells don't exist outside display)
                pass
        return alive_neighbors

    # Begins the evolution process
    def evolve(self):
        # grid_cache stores the new grid's data
        grid_cache = [[0 for _ in range(rows)] for _ in range(columns)]
        for x in range(rows):
            for y in range(columns):
                alive_neighbors = self.count_neighbors(x, y)
                if self.grid[x][y] == 1:
                    # alive cells with less than 2 neighbors but more than 3, DIE...
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        grid_cache[x][y] = 0
                        self.color_cell(dead, x, y)
                    else:
                        # alive cells with 2 or 3 neighbors LIVE ON
                        grid_cache[x][y] = self.grid[x][y]
                        self.color_cell(alive, x, y)
                elif self.grid[x][y] == 0:
                    # empty-cells with 3 neighbors SPAWN
                    if alive_neighbors == 3:
                        grid_cache[x][y] = 1
                        self.color_cell(alive, x, y)
        # returns a finished frame of the grid
        return grid_cache

    # randomly infects board with alive cells
    def infect(self):
        for x in range(rows):
            for y in range(columns):
                # 10% chance of birth
                schrodinger_cell = random.randint(1, 10)
                # determine if alive(1) or dead(0)
                schrodinger_cell = 0 if schrodinger_cell > 1 else 1
                # Give birth to schrodinger_cells
                self.grid[x][y] = schrodinger_cell
                # assign colors
                if self.grid[x][y] == 1:
                    self.color_cell(alive, x, y)
                else:
                    self.color_cell(dead, x, y)


# Screen is a square
screen_size = 500
screen = pygame.display.set_mode((screen_size, screen_size))
cell_size = 10

rows = int(screen_size / cell_size)
columns = int(screen_size / cell_size)

dead = (0, 0, 0)
alive = (255, 255, 255)


def main():
    # initialize game
    pygame.init()
    pygame.display.set_caption("Game Of Life")
    print("- Game Started -")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Set background to black
    screen.fill(dead)

    # Create 2 dimensional array. Array = a list of lists.
    grid = [[0 for _ in range(rows)] for _ in range(columns)]

    # Loop until the user clicks the close button
    done = False
    # infect board at beginning of game
    infected = False
    # toggle evolution
    run_program = True

    # ---- Main event loop ----
    while not done:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Toggle program via space bar
            elif pressed[pygame.K_SPACE]:
                run_program = not run_program
            # User clicks to infect squares
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                y = pos[0] // cell_size
                x = pos[1] // cell_size
                # Set that location to one
                grid[x][y] = 1
                Cells(grid).color_cell(alive, x, y)

        # Initial infection function. This is optional
        if not infected:
            Cells(grid).infect()
            infected = True

        if run_program:
            grid = Cells(grid).evolve()

        # Update screen
        pygame.display.flip()
        # Sets the frames per second
        clock.tick(10)

if __name__ == "__main__":
    main()