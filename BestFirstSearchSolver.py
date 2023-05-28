from Utils import *


# Data about best cell
class BestCellData:
    def __init__(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

    def set_data(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

class BestFirstSolver:

    def __init__(self, mat_string) -> None:

        assert len(mat_string) == 81

        self.matrix = [[0 for _ in range(9)] for _ in range(9)]

        for i in range(81):
            self.matrix[i // 9][i % 9] = int(mat_string[i])

    def Solve(self):
        cont = [True]

        # Check if its possible to have a solution
        for i in range(9):
            for j in range(9):
                if not self.is_correct_num(i, j):
                    # return if its not possible to have a solution
                    return

        # If its possible then try to solve the sudoku puzzle
        self.recursive_helper(cont)

        # -------------------- 注意 ------------------- 
        # TODO: 你可以把下面这行代码取消 / 增加注释，以此来显示每个棋盘的求解结果
        cmd_Visualization("".join(map(str, sum(self.matrix, []))))
    
    
    # Helper function for best first search
    def recursive_helper(self, cont):
        # 1st stopping point
        if not cont[0]:
            return
        
        # Best entry or one with least possibilities for a cell
        best_candidate = BestCellData(-1, -1, 100)
        for r in range(9):
            for c in range(9):
                # not filled
                if self.matrix[r][c] == 0:
                    num_choices = self.count_choices(r, c)

                    if best_candidate.choices > num_choices:
                        best_candidate.set_data(r, c, num_choices)

        # if not choices were found:
        # then board is filled - best first search is done. The solution depends on not have a zero value. If all board is non zero then solution is found
        if best_candidate.choices == 100:
            # set the flag to stop recursive calls
            cont[0] = False
            return

        row = best_candidate.row
        col = best_candidate.col

        # If best candidate found then try to fill 1-9
        for num in range(1, 10):  # will only go to 9

            # 2nd stopping point
            if not cont[0]:
                return

            self.matrix[row][col] = num

            if self.is_correct_num(row, col):
                self.recursive_helper(cont)  # recursion

        # 3rd stopping point
        if not cont[0]:
            return

        # Since we did not find the correct number then backtrack, change the value to 0 once again
        self.matrix[row][col] = 0

    # count number of choice that haven't been used

    def count_choices(self, i, j):
        can_pick = [True, True, True, True, True, True,
                    True, True, True, True]  # from 0 to 9 - drop 0

        # check row
        for k in range(9):
            can_pick[self.matrix[i][k]] = False

        # check col
        for k in range(9):
            can_pick[self.matrix[k][j]] = False

        # check 3 x 3 square
        r = i // 3
        c = j // 3
        for row in range(r*3, r*3+3):
            for col in range(c*3, c*3+3):
                can_pick[self.matrix[row][col]] = False

        # Count
        count = 0
        for k in range(1, 10):  # 1 to 9
            if can_pick[k]:
                count += 1

        return count

    def is_correct_num(self, row, col):
        # check row
        for c in range(9):
            if self.matrix[row][col] != 0 and col != c and self.matrix[row][col] == self.matrix[row][c]:
                return False

            # check column
        for r in range(9):
            if self.matrix[row][col] != 0 and row != r and self.matrix[row][col] == self.matrix[r][col]:
                return False

        # Check 3 x 3 matrix
        r = row // 3
        c = col // 3

        for i in range(r*3, r * 3 + 3):
            for j in range(c * 3, c * 3 + 3):
                if row != i and col != j and self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[row][col]:
                    return False
        return True

# return true if the whole board has been occupied by non zero number - That will be the solution

    def is_board_solved(self):
        for r in range(9):
            for c in range(9):
                if self.matrix[r][c] == 0:
                    return False
        # cmd_Visualization("".join(map(str, sum(self.matrix, []))))
        return True


if __name__ == "__main__":

    grids = []
    with open("./data.txt") as f:
        for line in f.readlines():
            grids.append(line.strip())

    t1 = time.time()

    for grid in grids:
        sudo_1 = BestFirstSolver(grid)
        sudo_1.Solve()

    t2 = time.time()
    print("Total time: {:.4} s".format(t2 - t1))
