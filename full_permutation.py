from DFSsolver import std_dfs_solver
from Utils import *
import copy

class every_avail_solver(std_dfs_solver):

    def __init__(self, grid):

        self.grid = grid
        self.complete = False
        self.rowbit = [0 for _ in range(9)]
        self.colbit = [0 for _ in range(9)]
        self.block = [0 for _ in range(9)]
        self.lg = [0 for _ in range(1024)]
        self.pos = []
        self.results = []
        for i in range(9):
            self.lg[ 1 << i ] = i + 1

    def lowbit(self, x):
        return x & (-x)

    def getblk(self, x, y):
        return (x // 3) * 3 + y // 3

    def DFS(self, idx):
        if idx == len(self.pos):
            self.results.append(copy.deepcopy(self.grid))
            return 

        else:
            (row, col) = self.pos[idx]
            avail = self.rowbit[row] & self.colbit[col] & self.block[self.getblk(row, col)]
            while avail:
                number = self.lowbit(avail)
                avail ^= number
                number = self.lg[number]
                
                self.grid[row][col] = number

                self.block[self.getblk(row, col)] ^= (1 << (number - 1))
                self.rowbit[row] ^= (1 << (number - 1))
                self.colbit[col] ^= (1 << (number - 1))
                

                self.DFS(idx + 1)
                if not self.complete:
                    self.grid[row][col] = 0
                    self.block[self.getblk(row, col)] ^= ( 1 << ( number - 1 ))
                    self.rowbit[row] ^= (1 << ( number - 1))
                    self.colbit[col] ^= (1 << ( number - 1))
                    
                else:
                    break
        

    @runtime_display
    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    # print(self.getblk(i, j))
                    self.block[self.getblk(i, j)] |= (1 << (self.grid[i][j] - 1))
                    self.rowbit[i] |= (1 << (self.grid[i][j] - 1))
                    self.colbit[j] |= (1 << (self.grid[i][j] - 1))
                else:
                    self.pos.append((i, j))
        
        
        for i in range(9):
            self.block[i] = ((1 << 9) - 1) ^ self.block[i]
            self.rowbit[i] = ((1 << 9) - 1) ^ self.rowbit[i]
            self.colbit[i] = ((1 << 9) - 1) ^ self.colbit[i]
        self.DFS(0)



if __name__ == '__main__':
    # grid_str = "210000700300004020000080901000002050006000300040600000108030000090500000002000017"
    grid_str = "002400006030010000500008000007000002010000030900600400000007001000090080400200500"
    grid4diff = Str2Lst(grid_str)

    dfs_3 = every_avail_solver(grid4diff)
    dfs_3.solve()
    # print(dfs_3.results)
    print(len(dfs_3.results))
    for r in dfs_3.results:
        Arr = Lst2Str(r)
        cmd_Visualization(Arr)
    