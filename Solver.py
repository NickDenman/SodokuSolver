import numpy as np
import time as time

# Load sudokus
sudokus = np.load("resources/data/sudokus.npy")
sudokus1000 = np.load("resources/data/sudokus1000.npy")
sudokus_unsolvable = np.load("resources/data/sudokus_unsolvable.npy")

print("Shape of sudokus array:", sudokus.shape, "; Type of array values:", sudokus.dtype)

# Load solutions
solutions = np.load("resources/data/solutions.npy")
print("Shape of solutions array:", solutions.shape, "; Type of array values:", solutions.dtype, "\n")



def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
       sudoku : 9x9 numpy array of integers
           Empty cells are designated by 0.

    Output
       9x9 numpy array of integers
           It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    unsolvable = False
    temp = np.zeros((10,9,9), np.int32)


    # Check for any rows/cols with one value missing
    #oneMissingValueCheck(sudoku)
    # Fill in temp array with known values
    #for i in range(0, 10):
       #temp[i] = sudoku

    temp[0] = sudoku

    global updated
    updated = True

    while updated:
        updated = False
        for a in range(0, 9):
            temp = set_row(temp, a)

        for b in range(0, 9):
            temp = set_col(temp, b)

        for c in range(0, 3):
            for d in range(0,3):
                temp = set_grid(temp, c, d)

    if unsolvable == True:
        print("sudoku is unsolvable")

    solved_sudoku = temp[0]

    return solved_sudoku


def set_row(sudoku, row):
    unknownvals = np.setdiff1d(range(1,10), sudoku[0, row])
    for i in range(0, len(unknownvals)):
        for j in range(0, 9):
            if sudoku[0, row, j] == 0:
                if check_col(sudoku, j, unknownvals[i]):
                    if check_grid(sudoku, row, j, unknownvals[i]):
                        sudoku[unknownvals[i], row, j] = unknownvals[i]

    one_value_row(sudoku, row)
    val_once_in_row(sudoku, row)

    return sudoku


def set_col(sudoku, col):
    unknownvals = np.setdiff1d(range(1,10), sudoku[0, :, col])
    for i in range(0, len(unknownvals)):
        for j in range(0, 9):
            if sudoku[0, j, col] == 0:
                if check_row(sudoku, j, unknownvals[i]):
                    if check_grid(sudoku, j, col, unknownvals[i]):
                        sudoku[unknownvals[i], j, col] = unknownvals[i]

    one_value_col(sudoku, col)
    val_once_in_col(sudoku, col)

    return sudoku


def set_grid(sudoku, row, col):
    if row < 3:
       startRow = 0
    elif row < 6:
       startRow = 3
    else:
       startRow = 6

    if col < 3:
       startCol = 0
    elif col< 6:
       startCol = 3
    else:
       startCol = 6

    # Find missing values
    unknownvals = np.setdiff1d(range(1, 10), sudoku[0, startRow:startRow+3, startCol: startCol+3])
    for i in range(0, len(unknownvals)):
       for j in range(startRow, startRow + 3):
           for k in range(startCol, startCol + 3):
               if sudoku[0, j, k] == 0:
                   if check_row(sudoku, j, unknownvals[i]):
                       if check_col(sudoku, k, unknownvals[i]):
                           sudoku[unknownvals[i], j, k] = unknownvals[i]

    one_value_grid(sudoku, row, col)
    val_once_in_grid(sudoku, row, col)

    return sudoku


def check_row(sudoku, row, i):
    for col in range(0, 9):
        if i == sudoku[0, row, col]:
            return False

    return True


def check_col(sudoku, col, i):
    for row in range(0, 9):
        if i == sudoku[0, row, col]:
            return False

    return True


def check_grid(sudoku, row, col, num):
    if row < 3:
        startrow = 0
    elif row < 6:
        startrow = 3
    else:
        startrow = 6

    if col < 3:
        startcol = 0
    elif col < 6:
        startcol = 3
    else:
        startcol = 6

    for i in range(startrow, startrow + 3):
        for j in range(startcol, startcol + 3):
            if sudoku[0, i, j] == num:
                return False

    return True


def one_value_row(sudoku, row):
    for i in range(0,9):
        if sudoku[0, row, i] == 0:
            count = 0
            num = 1
            while num < 10 and count < 2:
                if sudoku[num, row, i] != 0:
                    count += 1
                    grid = num

                num += 1

            if count == 1:
                sudoku[0, row, i] = sudoku[grid, row, i]
                update_possibilities(sudoku, row, i, sudoku[grid, row, i])


def one_value_col(sudoku, col):
    for i in range(0,9):
        if sudoku[0, i, col] == 0:
            count = 0
            num = 1
            while num < 10 and count < 2:
                if sudoku[num, i, col] != 0:
                    count += 1
                    grid = num

                num += 1

            if count == 1:
                sudoku[0, i, col] = sudoku[grid, i, col]
                update_possibilities(sudoku, i, col, sudoku[grid, i, col])


def one_value_grid(sudoku, row, col):
    if row < 3:
        startrow = 0
    elif row < 6:
        startrow = 3
    else:
        startrow = 6

    if col < 3:
        startcol = 0
    elif col < 6:
        startcol = 3
    else:
        startcol = 6


    for i in range(startrow, startrow + 3):
        for j in range(startcol, startcol + 3):
            if sudoku[0, i, j] == 0:
                count = 0
                num = 1
                while num < 10 and count < 2:
                    if sudoku[num, i, j] != 0:
                        count += 1
                        grid = num

                    num += 1

                if count == 1:
                    sudoku[0, i, j] = sudoku[grid, i, j]
                    update_possibilities(sudoku, i, j, sudoku[grid, i, j])


def val_once_in_row(sudoku, row):
    for i in range(1,10):
        count = 0
        col=0
        for j in range(0,9):
            if sudoku[i, row, j] == i:
                col = j
                count += 1

        if count == 1:
            sudoku[0, row, col] = i
            update_possibilities(sudoku, row, col, i)


def val_once_in_col(sudoku, col):
    for i in range(1, 10):
        count = 0
        row = 0
        for j in range(0, 9):
            if sudoku[i, j, col] == i:
                row = j
                count += 1

        if count == 1:
            sudoku[0, row, col] = i
            update_possibilities(sudoku, row, col, i)


def val_once_in_grid(sudoku, row, col):
    if row < 3:
        start_row = 0

    elif row < 6:
        start_row = 3

    else:
        start_row = 6

    if col < 3:
        start_col = 0

    elif col < 6:
        start_col = 3

    else:
        start_col = 6

    for i in range(1, 10):
        count = 0
        rowval = 0
        colval = 0
        for j in range(start_row, start_row + 3):
            for k in range(start_col, start_col + 3):
                if sudoku[i, j, k] == i:
                    rowval = j
                    colval = k
                    count += 1

        if count == 1:
            sudoku[0, rowval, colval] = i
            update_possibilities(sudoku, rowval, colval, i)


def update_possibilities(sudoku, row, col, num):
    global updated
    updated = True
    if row < 3:
        startRow = 0
    elif row < 6:
        startRow = 3
    else:
        startRow = 6

    if col < 3:
        startCol = 0
    elif col < 6:
        startCol = 3
    else:
        startCol = 6

    for i in range(0,9):
        sudoku[num, i, col] = 0
        sudoku[num, row, i] = 0
        sudoku[num, (i // 3) + startRow, (i % 3) + startCol] = 0


def print_sudoku(sudoku):
    for i in range(0,9):
        if i%3==0:
            print("+-------+-------+-------+")
        for j in range(0,9):
            if j%3 == 0:
                print("| ", end='')

            print(sudoku[i, j], end='')
            print(" ", end='')
        print("| ")

    print("+-------+-------+-------+")

def check_sudoku(sudoku):
    for i in range(0, 9):
        row_sum = 0
        col_sum = 0
        grid_sum = 0
        for j in range(0, 9):
            row_sum += sudoku[i, j]
            col_sum += sudoku[j, i]
            grid_sum += sudoku[(j//3) + ((i%3)*3), (j%3) + ((i%3)*3)]

        if row_sum != 45 and col_sum != 45 and grid_sum != 45:
            return False

    return True


s = time.time()
for i in range(0, len(sudokus)):
    (np.array_equal(sudoku_solver(sudokus[i]), solutions[i]))

e = time.time()
print(e-s)