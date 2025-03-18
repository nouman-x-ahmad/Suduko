# NOUMAN AHMAD


import random as rnd

#============================================================================================================================================
def GEN_SUDUKO_GRID_MAP():

    randomized_val=0;
    num_grid_size = 9
    grid = [[{} for x in range(num_grid_size)] for y in range(num_grid_size)]




    for q in range(num_grid_size):
        for w in range(num_grid_size):
            grid[q][w] = 0




    for j in range(0, 9, 3):

        RND_BLOCK_NUMB = list(range(1, 10))  # Possible values for the block
        rnd.shuffle(RND_BLOCK_NUMB)  # Shuffle the values
        for k in range(0, 9, 3):
            grid[j][k] = RND_BLOCK_NUMB.pop()

    # Fill the remaining cells using backtracking
    REMAINING_GRID_FILLING(grid, 0, 3)

    # Randomly remove some values to create empty cells (2 to 4 values per block)
    for loopy in range(0, 9, 3):
        for loopx in range(0, 9, 3):
            RND_BLOCK_NUMB = [(row, col) for row in range(loopy, loopy + 3) for col in range(loopx, loopx + 3)]
            rnd.shuffle(RND_BLOCK_NUMB)
            num_to_remove = rnd.randint(1, 2)  # Randomly choose the number of values to remove
            for k in range(num_to_remove):
                Rank, File = RND_BLOCK_NUMB.pop()
                grid[Rank][File] = 0  # Empty cell

    return grid

#============================================================================================================================================
def REMAINING_GRID_FILLING(grid_map, rank, fill):

    temp=0
    substitute=0
    if fill >= 9:
        rank += 1
        fill = 0




    if rank >= 9:
        return True

    if grid_map[rank][fill] != 0:
        return REMAINING_GRID_FILLING(grid_map, rank, fill + 1)

    for x_val in range(1, 10):
        if check_safety(grid_map, rank, fill, x_val):
            grid_map[rank][fill] = x_val
            if REMAINING_GRID_FILLING(grid_map, rank, fill + 1):
                return True
            grid_map[rank][fill] = 0

    return False

#============================================================================================================================================
def check_safety(grid, row, col, value):
    # Check row
    if value in grid[row]:
        return False

    # Check column
    if value in [grid[i][col] for i in range(9)]:
        return False

    # Check 3x3 box
    GRID_BOX_RANK = row // 3
    GRID_BOX_FILE = col // 3

    for loop in range(GRID_BOX_RANK * 3, GRID_BOX_RANK * 3 + 3):

        for iter in range(GRID_BOX_FILE * 3, GRID_BOX_FILE * 3 + 3):

            if grid[loop][iter] == value:

                return False

    # If value does not exist in the current box, return True (valid)
    return True

#============================================================================================================================================

# Function to print the Sudoku grid
def print_sudoku(grid):

    for x, row in enumerate(grid):
        if x % 3 == 0 and x != 0:
            print("-" * 21)  # Print horizontal boundary between blocks


        for y, grid_block_cell in enumerate(row):
            if y % 3 == 0 and y != 0:
                print("|", end=" ")  # Print vertical boundary within blocks



            if grid_block_cell != 0:
                # Print the cell value followed by a space
                print(grid_block_cell, end=" ")
            else:
                # Printing a dash "-" to represent an empty cell followed by a space
                print("-", end=" ")
        print()


#============================================================================================================================================




sudoku_gridz = GEN_SUDUKO_GRID_MAP()
# print("Generated Sudoku Grid:")
# print_sudoku(sudoku_gridz)
