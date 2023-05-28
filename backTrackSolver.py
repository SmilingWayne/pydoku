from Utils import *


class standard_solver:
    def __init__(self, mat_string):
        assert len(mat_string) == 81
        self.matrix = [[0 for _ in range(9)] for _ in range(9)]
        # 初始化
        for i in range(81):
            self.matrix[i // 9][i % 9] = int(mat_string[i])
        self.tmp_matrix = self.matrix

    def check(self,  y, x, n):
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

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.matrix[y0 + i][x0 + j] == n:
                    return False

        return True

    # @runtime_display
    def Solve(self):
        res = self.backtrack_solver()

        
        # -------------------- 注意 ------------------- 
        # TODO: 你可以把下面这行代码取消 / 增加注释，以此来显示每个棋盘的求解结果

        cmd_Visualization("".join(map(str, sum(self.matrix, []))))
        return res

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
                        if self.check(i, j, n):  # 检查 i j处可不可填n
                            self.matrix[i][j] = n  # 可以，就写成n
                            self.tmp_matrix = self.backtrack_solver()
                            if self.tmp_matrix is not None:
                                self.matrix = self.tmp_matrix
                                return self.tmp_matrix
                            self.matrix[i][j] = 0
                    return None
        return self.matrix


if __name__ == "__main__":

    grids = []
    with open("./data.txt") as f:
        for line in f.readlines():
            grids.append(line.strip())

    t1 = time.time()

    for grid in grids:
        sd = standard_solver(grid)
        res = sd.Solve()

    t2 = time.time()
    print("Total time: {:.4} s".format(t2 - t1))

    # t1 = "008209070705000060009607803070085020500020708280004050601402007900000100002300604"
    # sd = standard_solver(t1)
    # result = sd.Solve()
    # a = "".join(map(str, sum(result, [])))
    # cmd_Visualization(a)
