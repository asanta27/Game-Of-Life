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


def main():
    # Define colors
    dead = (0, 0, 0)
    alive = (255, 255, 255)
    color_state = dead

    # initialize game
    pygame.init()
    pygame.display.set_caption("Game Of Life")

    # Set width and height of screen. size = (width, height)
    size = (505, 505)
    screen = pygame.display.set_mode(size)

    # Set width, height and margin of cells
    cellx = 20
    celly = 20
    margin = 5

    # Create 2 dimensional array. Array = a list of lists.
    grid = [[0 for x in range(20)] for y in range(20)]

    # Long version
    """
        # Create an empty list
        grid = []
        # Loop for each row
        for row in range(10):
            # For each row, create a list that will represent an entire row
            grid.append([])
            
            # Loop for each column
            for column in range(10):
                # Add a the number zero to the current row
                grid[row].append(0)
        """

    # Loop until the user clicks the close button
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while not done:
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Set background to black
        screen.fill(dead)

        # Begin drawing cells
        for row in range(20):
            for column in range(20):

                # testing alive cell
                grid[1][5] = 1
                if grid[row][column] == 1:
                    color_state = alive

                # draw cells
                pygame.draw.rect(screen,
                                 color_state,
                                 [(margin + cellx) * column + margin,
                                  (margin + celly) * row + margin,
                                  cellx,
                                 celly])

        # Update screen
        pygame.display.flip()

        # Sets the frames per second
        clock.tick(10)

if __name__ == '__main__':
    main()