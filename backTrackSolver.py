from Utils import *

class standard_solver:
    def __init__(self, matrix):
        self.matrix = matrix
        self.tmp_matrix = matrix
        
    def check(self,  y, x, n ):
        """_summary_

            check whether n is valid in matrix[y][x]
        Args:
            matrix (_ipt matrx_): _description_
            y (_row_): _description_
            x (_col_): _description_
            n (_num_): _description_

        Returns:
            _bool_: _whether its okay_
        """
        for i in range(9):
            if self.matrix[y][i] == n:
                return False
        for i in range(9):
            if self.matrix[i][x] == n:
                return False

        x0 = (x//3) * 3
        y0 = (y//3) * 3
        
        for i in range(3):
            for j in range(3):
                if self.matrix[y0 + i][x0 + j] == n:
                    return False

        return True

    def backtrack_solver(self):
        """_summary_

        Args:
            matrix (_list[list[int]]_): _description_

        Returns:
            _matrix_: _solved sudoku)
        """
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    for n in range(1, 10):
                        if self.check( i, j, n):
                            self.matrix[i][j] = n
                            self.tmp_matrix = self.backtrack_solver()                  
                            if self.tmp_matrix is not None:
                                self.matrix = self.tmp_matrix
                                return self.tmp_matrix
                            self.matrix[i][j] = 0
                    return None
        return self.matrix

class diagnoal_solver(standard_solver):
    def __init__(self, grid, constraints):
        standard_solver.__init__(self, grid)
        self.constraints = constraints
    
    def check(self, y, x, n):
        """_summary_

        Args:
            y (_type_): _description_
            x (_type_): _description_
            n (_type_): _description_
        """

        for i in range(9):
            if self.matrix[y][i] == n:
                return False
        for i in range(9):
            if self.matrix[i][x] == n:
                return False

        x0 = (x//3) * 3
        y0 = (y//3) * 3
        
        for i in range(3):
            for j in range(3):
                if self.matrix[y0 + i][x0 + j] == n:
                    return False

        for (_, constraint) in self.constraints.items():
            if (y, x) in constraint:
                for fill in list(constraint):
                    (y1, x1) = fill
                    if self.matrix[y1][x1] == n:
                        return False

        return True

if __name__ == "__main__":
    test = [[6, 3, 2, 0, 0, 4, 7, 8, 0],
          [9, 0, 5, 0, 8, 2, 6, 3, 1],
          [8, 0, 0, 0, 6, 3, 0, 0, 2],
          [0, 6, 1, 3, 0, 7, 2, 0, 0],
          [0, 9, 0, 8, 0, 6, 0, 1, 0],
          [0, 0, 4, 2, 0, 5, 9, 6, 0],
          [1, 0, 0, 4, 2, 0, 0, 0, 6],
          [3, 2, 6, 5, 7, 0, 8, 0, 4],
          [0, 7, 9, 6, 0, 0, 1, 2, 5]]

    diagnoal = "000120040204000000003040060500000100000070000002000008010090800000000506070016000"
    diagnoal_constraints = {
            "0":set([(3,0),(2, 1),(1, 2),(0, 3)]),
            "1":set([(4,0),(3, 1),(2, 2),(1, 3), (0, 4)]),
            "2":set([(0,4),(1, 5),(2, 6),(3, 7), (4, 8)]),
            "3":set([(0,5),(1, 6),(2, 7),(3, 8)]),
            "4":set([(4,8),(5, 7),(6, 6),(7, 5), (8, 4)]),
            "5":set([(5,8),(6, 7),(7, 6),(8, 5)]),
            "6":set([(8,4),(7, 3),(6, 2),(5, 1), (4, 0)]),
            "7":set([(8,3),(7, 2),(6, 1),(5, 0)]),
    }

    # bdfs = standard_solver(matrix =test)
    # bdfs.backtrack_solver()
    # Arr = Lst2Str(bdfs.grid)
    # print(Arr)
    # print(bdfs.grid)

    # bts = standard_solver(test)
    # bts.backtrack_solver()
    grid = Str2Lst(diagnoal)
    diag_solver = diagnoal_solver(grid, diagnoal_constraints)
    diag_solver.backtrack_solver()
    Arr = Lst2Str(diag_solver.matrix)
    cmd_Visualization(Arr)
    