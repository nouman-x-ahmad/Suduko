#NOUMAN AHMAD


from collections import defaultdict

from suduko_map import sudoku_gridz





step_count_iterator = 0
#============================================================================================================================================
grid_size=9
def empty_box_finder(suduko_grid_map):
    for x in range(grid_size):
        for y in range(grid_size):
            if suduko_grid_map[x][y] == 0:
                return x, y
    return None, None


#============================================================================================================================================


def check_validity(suduko_grid_map, num, pos):
    # Check row
    if num in suduko_grid_map[pos[0]]:
        return False

    # Check column
    if num in [suduko_grid_map[i][pos[1]] for i in range(grid_size)]:
        return False

    # Check box
    box_row = pos[0] // 3
    box_col = pos[1] // 3

    if num in [suduko_grid_map[i][j] for i in range(box_row * 3, box_row * 3 + 3) for j in range(box_col * 3, box_col * 3 + 3)]:
        return False

    return True


#============================================================================================================================================

def solve_sudoku(boardz):
    global step_count_iterator
    step_count_iterator += 1

    row, col = empty_box_finder(boardz)
    board_map_printer(boardz)


    print(f" \n count: {step_count_iterator}")
    if row is None:
        print("\nSolution found after", step_count_iterator, "steps!")
        return True

    domains = get_domains(boardz)


    if not domains:
        return False

    mrv_pos = min(domains.items(), key=lambda x: len(x[1]))
    order = sorted(mrv_pos[1], key=lambda x: -len(suduko_degree_heuristic_val_finder(boardz, x, mrv_pos[0])))

    for num in order:
        if check_validity(boardz, num, mrv_pos[0]):
            boardz[mrv_pos[0][0]][mrv_pos[0][1]] = num

            if solve_sudoku(boardz):

                return True

            boardz[mrv_pos[0][0]][mrv_pos[0][1]] = 0

    return False

#============================================================================================================================================


def get_domains(suduko_grid_map):
    domains = defaultdict(set)
    for i in range(grid_size):
        for j in range(grid_size):
            if suduko_grid_map[i][j] == 0:
                for n in range(1, grid_size+1):
                    if check_validity(suduko_grid_map, n, (i, j)):
                        domains[(i, j)].add(n)
    return domains


#============================================================================================================================================

def suduko_degree_heuristic_val_finder(suduko_grid_map, temp, cordintor):
    degree = set()
    row, col = cordintor

    # Check row
    for j in range(grid_size):
        if suduko_grid_map[row][j] == 0 and j != col:
            degree.add((row, j))

    # Check column
    for i in range(grid_size):
        if suduko_grid_map[i][col] == 0 and i != row:
            degree.add((i, col))

    # Check box
    box_row = row // 3
    box_col = col // 3

    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):

            if (i, j) != cordintor and  suduko_grid_map[i][j] == 0 :
                degree.add((i, j))


    return degree

#============================================================================================================================================


def arc_cons_3(suduko_grid_map):
    domains = get_domains(suduko_grid_map)
    queue_z = [(pos, var) for pos, vars in domains.items() for var in vars]

    while queue_z:
        pos, var = queue_z.pop(0)
        if recheck_map(suduko_grid_map, var, pos, domains):
            if not domains[pos]:
                return False
            neighbors = neighbour_finder(suduko_grid_map, pos)
            queue_z.extend([(neighbor, var) for neighbor in neighbors])

    return True

#============================================================================================================================================


def recheck_map(suduko_grid_map, var, cordinates, domains):
    revised = False
    row, col = cordinates

    # Check row
    for j in range(grid_size):
        if suduko_grid_map[row][j] == var and j != col:
            domains[cordinates].remove(var)
            revised = True

    # Check column
    for rank in range(grid_size):
        if suduko_grid_map[rank][col] == var and rank != row:
            domains[cordinates].remove(var)
            revised = True

    # Check box
    rank_row = row // 3
    file_col = col // 3
    for rank in range(rank_row * 3, rank_row * 3 + 3):
        for file in range(file_col * 3, file_col * 3 + 3):
            if suduko_grid_map[rank][file] == var and (rank, file) != cordinates:
                domains[cordinates].remove(var)
                revised = True

    return revised

#============================================================================================================================================


def neighbour_finder(board, cordinator):
    row, col = cordinator
    neighbors = set()

    # Check row
    for j in range(grid_size):
        if j != col and board[row][j] == 0:
            neighbors.add((row, j))

    # Check column
    for rank in range(grid_size):
        if rank != row and board[rank][col] == 0:
            neighbors.add((rank, col))

    # Check box
    box_row = row // 3
    box_col = col // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if (i, j) != cordinator and board[i][j] == 0:
                neighbors.add((i, j))

    return neighbors

#============================================================================================================================================


def board_map_printer(board):
    for i in range(grid_size):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(grid_size):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else "-", end=" ")
        print()



#============================================================================================================================================


sudoku_grid = sudoku_gridz
print("Original Sudoku Grid:")
board_map_printer(sudoku_grid)

print("\nSolving the Sudoku puzzle...")

arc_cons_3(sudoku_grid)
if not solve_sudoku(sudoku_grid):
    print("\nNo solution found for the given Sudoku puzzle.")
else:
    print("\nSolved Sudoku Grid:")
    board_map_printer(sudoku_grid)