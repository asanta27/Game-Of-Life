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

# neighbor coordinates
neighbor_coordinates = {
    (0,1),   # Top
    (1, 1),  # Top-Right
    (1, 0),  # Right
    (1,-1),  # Bottom-Right
    (0,-1),  # Bottom
    (-1,-1), # Bottom-Left
    (-1,0),  # Left
    (-1,1)   # Top-Left
}

# Define colors
dead = (0, 0, 0)
alive = (255, 255, 255)

# Set width and height of screen. size = (width, height)
size = (500, 500)
screen = pygame.display.set_mode(size)

# Set width, height and margin of cells
cellx = 5
celly = 5


# OPTIONAL: randomly infects board.
def infect_board(grid):
    for row in range(100):
        for column in range(100):

            rand = random.randint(1, 10) # 10% chance
            if rand > 1:
                rand = 0

            grid[row][column] = rand # determine if alive(1) or dead(0)

            if grid[row][column] == 1:
                color_cell(alive, row, column)
            else:
                color_cell(dead, row, column)


# assigns color to a specific cell
def color_cell(color_state, row, column):
    pygame.draw.rect(screen,
                     color_state,
                     [cellx * column,
                      celly * row,
                      cellx,
                      celly])


# Counts alive-neighbors of chosen cell
def count_neighbors(grid, x, y):
    alive_neighbors = 0

    for i in neighbor_coordinates:
        # NeighborX and NeighborY coordinates
        nx = i[0]
        ny = i[1]
        try:
            if grid[x + nx][y + ny] == 1:
                alive_neighbors = alive_neighbors + 1
        except:
            # Handles errors from cells that are on the edge of the board
            # Error comes from index being out of range (cells don't exist outside display)
            pass
    return alive_neighbors


# Begins the evolution process
def evolve(grid):
    # grid_cache stores the new grid's data
    grid_cache = [[0 for x in range(100)] for y in range(100)]
    for x in range(100):
        for y in range(100):
            alive_neighbors = count_neighbors(grid, x, y)
            if grid[x][y] == 1:
                # alive cells with less than 2 neighbors but more than 3, DIE...
                if alive_neighbors < 2 or alive_neighbors > 3:
                    grid_cache[x][y] = 0
                    color_cell(dead, x, y)
                else:
                    # alive cells with 2 or 3 neighbors LIVE ON
                    grid_cache[x][y] = grid[x][y]
                    color_cell(alive, x, y)
            elif grid[x][y] == 0:
                # empty-cells with 3 neighbors SPAWN
                if alive_neighbors == 3:
                    grid_cache[x][y] = 1
                    color_cell(alive, x, y)
            else:
                pass
    # returns the latest grid
    return grid_cache


def main():
    print("- Game Started -")
    # initialize game
    pygame.init()
    pygame.display.set_caption("Game Of Life")

    # Create 2 dimensional array. Array = a list of lists.
    grid = [[0 for x in range(100)] for y in range(100)]

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set background to black
    screen.fill(dead)

    # Loop until the user clicks the close button
    done = False

    # infect board at beginning of game
    infected = False

    # toggle evolution
    run_program = False

    # ---- Main event loop ----
    while not done:

        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // cellx
                row = pos[1] // celly
                # Set that location to one
                grid[row][column] = 1
                color_cell(alive, row, column)

            # Toggle program via space bar
            elif pressed[pygame.K_SPACE]:
                run_program = not run_program

        # Initial infection function. This is optional
        if not infected:
            infect_board(grid)
            infected = True

        if run_program:
            grid = evolve(grid)
            # Update screen
            pygame.display.flip()
        else:
            pygame.display.flip()

        # Sets the frames per second
        clock.tick(10)

if __name__ == '__main__':
    main()