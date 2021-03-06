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

    neighbor_coordinates = {
        (-1,-1),( 0,-1),(1,-1),
        (-1, 0),        (1, 0),
        (-1, 1),( 0, 1),(1, 1)
    }

    glider_gun = {
        (1, 7), (1, 8), (2, 7), (2, 8), (11, 7), (11, 8), (11, 9),
        (12, 10), (13, 11), (14, 11), (12, 6), (13, 5), (14, 5),
        (16, 6), (17, 7), (17, 8), (15, 8), (18, 8), (17, 9),
        (16, 10), (21, 7), (22, 7), (21, 6), (22, 6), (21, 5),
        (23, 4), (23, 8), (25, 4), (25, 3), (25, 8), (25, 9),
        (35, 6), (36, 6),(35, 5), (36, 5), (22, 5)
    }

    # Hit "G" for glider gun!
    def glider(self):
        for i in self.glider_gun:
            x = i[0]
            y = i[1]
            self.grid[x][y] =1
            self.color_cell(x, y)
        return self.grid

    # assigns color to a specific cell
    def color_cell(self, x, y):
        color = alive if self.grid[x][y] == 1 else dead
        pygame.draw.rect(screen,
                         color,
                         [(margin + cell_size) * x + margin,
                          (margin + cell_size) * y + margin,
                          cell_size, cell_size])

    # Counts alive-neighbors of chosen cell
    def count_neighbors(self, x, y):
        alive_neighbors = 0
        for i in self.neighbor_coordinates:
            # NeighborX and NeighborY coordinates
            nx = i[0]
            ny = i[1]
            try:
                # prevents counting "neighbors" on other side of board
                # when index is less than 0
                if (x+nx) < 0 or (y+ny) < 0:
                    pass
                # count neighbor if alive
                elif self.grid[x + nx][y + ny] == 1:
                    alive_neighbors += 1
            except:
                # Handles errors from cells that are on the edge of the board
                # Error comes from index being out of range (cells don't exist outside display)
                pass
        return alive_neighbors

    # Begins the evolution process
    def evolve(self):
        # grid_cache stores the next frame's data.
        grid_cache = [[0 for _ in range(rows)] for _ in range(columns)]
        for x in range(rows):
            for y in range(columns):
                # Update cell color to latest frame
                self.color_cell(x, y)
                # Count neighbors of this cell
                alive_neighbors = self.count_neighbors(x, y)
                if self.grid[x][y] == 1:
                    # alive cells with less than 2 neighbors but more than 3, DIE...
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        # Contains the data for the next frame.
                        grid_cache[x][y] = 0
                    else:
                        # alive cells with 2 or 3 neighbors LIVE ON
                        grid_cache[x][y] = self.grid[x][y]
                elif self.grid[x][y] == 0:
                    # empty-cells with 3 neighbors SPAWN
                    if alive_neighbors == 3:
                        grid_cache[x][y] = 1
        # returns the next frame of the grid
        return grid_cache

    # randomly seeds alive cells
    def seed(self):
        for x in range(rows):
            for y in range(columns):
                # 10% chance of birth
                schrodinger_cell = random.randint(1, 10)
                # determine if alive(1) or dead(0)
                schrodinger_cell = 0 if schrodinger_cell > 1 else 1
                # Give birth to schrodinger_cells
                self.grid[x][y] = schrodinger_cell
                # Update cell color
                self.color_cell(x, y)

# Screen is a square
screen_size = 500
screen = pygame.display.set_mode((screen_size, screen_size))

cell_size = 9
margin = 1

rows = int(screen_size / (cell_size + margin))
columns = int(screen_size / (cell_size + margin))

# Cell RGB colors
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

    # infects board at beginning of game
    Cells(grid).seed()

    # toggle evolution
    run_program = True

    # toggles the glider gun
    glider_toggle = True

    # Loop until the user clicks the close button
    done = False

    # ---- Main event loop ----
    while not done:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Toggle program via space bar
            elif pressed[pygame.K_SPACE]:
                run_program = not run_program
            # Hit "G" for glider_toggle!
            elif pressed[pygame.K_g]:
                    # reset cells
                    screen.fill(dead)
                    grid = [[0 for _ in range(rows)] for _ in range(columns)]
                    if glider_toggle:
                        Cells(grid).glider()
                        glider_toggle = False
                    else:
                        Cells(grid).seed()
                        glider_toggle = True
            # User clicks to spawn/kill cells
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Gets the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                x = pos[0] // (cell_size + margin)
                y = pos[1] // (cell_size + margin)
                # Toggle that cell
                grid[x][y] = 0 if grid[x][y] == 1 else 1
                # Update cell color
                Cells(grid).color_cell(x, y)

        if run_program:
            grid = Cells(grid).evolve()

        # Update screen
        pygame.display.flip()
        # Sets the frames per second
        clock.tick(10)

if __name__ == "__main__":
    main()
