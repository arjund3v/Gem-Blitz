from data_structures import Queue

def get_overflow_list(grid):
    rows = len(grid)
    cols = len(grid[0])
    overflow_list = []

    #  Iterate through all cells in the grid and find overflowing ones
    for i in range(rows):
        for j in range(cols):
            neighbors = 0
            if i == 0 or i == rows - 1:
                if j == 0 or j == cols - 1:
                    neighbors = 2
                else:
                    neighbors = 3
            elif j == 0 or j == cols - 1:
                neighbors = 3
            else:
                neighbors = 4

            if abs(grid[i][j]) >= neighbors:
                overflow_list.append((i, j))

    if overflow_list:
        return overflow_list
    else:
        return None


# Iterates through all cells of the grid and checks if all the signs are the same
def check_same_sign(grid):
    sign = None
    for row in grid:
        for cell in row:
            if cell != 0:
                if sign is None:
                    sign = 1 if cell > 0 else -1
                elif (cell > 0 and sign > 0) or (cell < 0 and sign < 0):
                    continue
                else:
                    return False
    return True


# Handle overflow and modify grid to reduce it
def overflow(grid, a_queue):
    overflow_list = get_overflow_list(grid)

    if not overflow_list or check_same_sign(grid):
        return 0

    new_grid = [[cell for cell in row] for row in grid]

    # Add one unit to neighbouts of overflowing cells
    for i, j in overflow_list:
         sign = -1 if grid[i][j] < 0 else 1
         neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
         for ni, nj in neighbors:
             if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                grid[ni][nj] = (abs(grid[ni][nj]) + 1) * sign

    # Remove units from overflowing cells
    for i, j in overflow_list:
        grid[i][j] -= new_grid[i][j]

    copied_grid = [row[:] for row in grid]
    a_queue.enqueue(copied_grid)
    return 1 + overflow(grid, a_queue)
