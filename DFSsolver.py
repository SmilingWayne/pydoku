from Utils import *

class opt_std_dfs_solver2:

    def __init__(self, grid):
        self.grid = Str2Lst(grid)
        self.map = [0 for _ in range(1 << 9)]
        self.ones = [0 for _ in range(1 << 9)]
        self.rowbit = [0 for _ in range(9)]
        self.colbit = [0 for _ in range(9)]
        self.cell = [[ 0 for _ in range(3)] for _ in range(3)]

    def initize(self):

        cnt = 0
        state = (1 << 9) - 1
        for i in range(9):
            self.rowbit[i] = state
            self.colbit[i] = state
            self.cell[i // 3][i % 3] = state

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.check(i, j , self.grid[i][j] - 1, True)
                else:
                    cnt += 1
        return cnt

    def get(self, x, y):
        return self.rowbit[x] & self.colbit[y] & self.cell[x // 3][y // 3]
    
    def lowbit(self, x):
        return x & (-x)

    def check(self, x, y, t, is_set):
        if is_set:
            self.grid[x][y] = 1 + t
            
        else:
            self.grid[x][y] = 0
        
        v = 1 << t
        if not is_set:
            v = -v
        self.rowbit[x] -= v
        self.colbit[y] -= v 
        self.cell[x // 3][y // 3] -= v


    def DFS(self, cnt):
        if not cnt:
            return True
        x_0 = y_0 = 0
        tmp = 0
        minv = 10
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    state = self.get(i, j)
                    if self.ones[state] < minv:
                        minv = self.ones[state]
                        tmp = state
                        x_0 = i
                        y_0 = j 
        
        while tmp:
            t = self.map[self.lowbit(tmp)]
            self.check(x_0, y_0, t , True)
            if self.DFS(cnt - 1):
                return True
            self.check(x_0, y_0, t , False)
            tmp -= self.lowbit(tmp)

        return False
    @runtime_display
    def solve(self):
        for i in range(9):
            self.map[1 << i] = i
        for i in range(1 << 9):
            j = i
            while j:
                self.ones[i] += 1
                j -= self.lowbit(j)
        
        k = self.initize()
        
        self.DFS(k)
    
class std_dfs_solver:
    """_summary_

        Use DFS to solve Sudoku - Standard

    """

    def __init__(self, grid):
        self.grid = Str2Lst(grid)
        self.complete = False
        self.rowbit = [0 for _ in range(9)]
        self.colbit = [0 for _ in range(9)]
        self.block = [0 for _ in range(9)]
        self.lg = [0 for _ in range(1024)]
        self.pos = []
        for i in range(9):
            self.lg[ 1 << i ] = i + 1

    def lowbit(self, x):
        return x & (-x)

    def getblk(self, x, y):
        return (x // 3) * 3 + y // 3

    def DFS(self, idx):

        if idx == len(self.pos):
            self.complete = True
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

class opt_std_dfs_solver(std_dfs_solver):
    def __init__(self, grid):
        std_dfs_solver.__init__(self, grid)
        

    def getPriority(self, x):
        (row, col) = x
        tmp_avail = self.rowbit[row] & self.colbit[col] & self.block[self.getblk(row, col)]
        return tmp_avail - ((tmp_avail >> 1) & 0x55555555)

    def DFS(self, idx):

        if idx == len(self.pos):
            self.complete = True
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
                    self.block[self.getblk(i, j)] |= (1 << (self.grid[i][j] - 1))
                    self.rowbit[i] |= (1 << (self.grid[i][j] - 1))
                    self.colbit[j] |= (1 << (self.grid[i][j] - 1))
                else:
                    self.pos.append((i, j))
        
        for i in range(9):
            self.block[i] = ((1 << 9) - 1) ^ self.block[i]
            self.rowbit[i] = ((1 << 9) - 1) ^ self.rowbit[i]
            self.colbit[i] = ((1 << 9) - 1) ^ self.colbit[i]
        
        sorted(self.pos,  key = lambda x : self.getPriority(x))
        self.DFS(0)

class diag_dfs_solver(std_dfs_solver):

    """_summary_
        Use DFS to solve Diag Sudoku - Support multiple diags
    """

    def __init__(self, grid, constraints):
        """_summary_

        Args:
            grid (_List[List[int]]_): _Input original Sudoku Grid_
            constraints (_Dict{ str: set() }_): _Diag constraints_
        """
        self.grid = Str2Lst(grid)
        self.rowbit = [0 for _ in range(9)]
        self.colbit = [0 for _ in range(9)]
        self.block = [0 for _ in range(9)]
        self.lg = [0 for _ in range(1024)]
        self.diagbit = []
        self.pos = []
        self.complete = False
        self.diagSet = set()
        self.constraints = constraints
        for i in range(9):
            self.lg[ 1 << i ] = i + 1

        for i in range(len(constraints)):
            self.diagbit.append(0)

        for (_, constraint) in self.constraints.items():
            self.diagSet |= constraint
        


    def check(self, ipt, row, col):
      
        for idx, (_, constraint) in enumerate(self.constraints.items()):
            if (row, col) in constraint:
                
                ipt &= self.diagbit[idx]
                
        return ipt
            
    @runtime_display
    def solve(self):

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.block[self.getblk(i, j)] |= (1 << (self.grid[i][j] - 1))
                    self.rowbit[i] |= (1 << (self.grid[i][j] - 1))
                    self.colbit[j] |= (1 << (self.grid[i][j] - 1))

                else:
                    self.pos.append((i, j))
        
        
        for idx, (_, constraint) in enumerate(self.constraints.items()):
            for (x_, y_) in constraint:
                if self.grid[x_][y_] != 0:
                    self.diagbit[idx] |= (1 << (self.grid[x_][y_] - 1))
        
        for i in range(9):
            self.block[i] = ((1 << 9) - 1) ^ self.block[i]
            self.rowbit[i] = ((1 << 9) - 1) ^ self.rowbit[i]
            self.colbit[i] = ((1 << 9) - 1) ^ self.colbit[i]
        
        for i in range(len(self.diagbit)):
            self.diagbit[i] = ((1 << 9) - 1) ^ self.diagbit[i]
        
        self.DFS(0)
        

    def DFS(self, idx):

        if idx == len(self.pos):
            self.complete = True
            
            return 

        else:
            # self.complete = True
            (row, col) = self.pos[idx]
            in_diagset = (row, col) in self.diagSet
            avail = self.rowbit[row] & self.colbit[col] & self.block[self.getblk(row, col)]
            
            if avail:
                
                if in_diagset :
                    avail = self.check(avail, row, col)
                    # print(bin(avail))
                    # print(row, col)

                while avail:
                    
                    number = self.lowbit(avail)
                    avail ^= number
                    number = self.lg[number]
                    self.grid[row][col] = number
                    self.block[self.getblk(row, col)] ^= (1 << (number - 1))
                    self.rowbit[row] ^= (1 << (number - 1))
                    self.colbit[col] ^= (1 << (number - 1))
                    if in_diagset:
                        for index, (_, constraint) in enumerate(self.constraints.items()):
                            if (row, col) in constraint:
                                self.diagbit[index] ^= (1 << ( number - 1))
                            

                    self.DFS(idx + 1)

                    if not self.complete:
                        self.grid[row][col] = 0
                        
                        self.block[self.getblk(row, col)] ^= ( 1 << ( number - 1 ))
                        self.rowbit[row] ^= (1 << ( number - 1))
                        self.colbit[col] ^= (1 << ( number - 1))
                        if in_diagset:
                            for index, (_, constraint) in enumerate(self.constraints.items()):
                                if (row, col) in constraint:
                                    self.diagbit[index] ^= (1 << ( number - 1))
                    else:
                        break

class jigsaw_dfs_solver:

    """
    arr :
    000006000907080016001300800200900000000053000000400000790014000350847020000100000
    ABBBBBBCDAABBBCCCDAAACCCDDDAEACCFFDGAEEFFFDDGEEFFFFDHGEEHHHHHHGEEIHIIHGGIIIIIIGGG
    """
    def __init__(self, arr, regions):
        self.grid = Str2Lst(arr)
        self.boxes = [[_ for _ in range(9)] for _ in range(9)]
        for i in range(81):
            self.boxes[i // 9][i % 9] = ord(regions[i]) - 65
        self.rowbit = [0 for _ in range(9)]
        self.colbit = [0 for _ in range(9)]
        self.block = [0 for _ in range(9)]
        self.lg = [0 for _ in range(1024)]
        self.complete = False
        self.pos = []
        for i in range(9):
            self.lg[ 1 << i ] = i + 1

    def lowbit(self, x):
        return x & (-x)

    def getblk(self, x, y):
        return self.boxes[x][y]

    def DFS(self, idx):
        if idx == len(self.pos):
            self.complete = True
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

# class killer_dfs_solver:
#     def __init__(self, cages, numbers):
#         self.cages = cages
#         self.grid = [[0 for _ in range(9)] for _ in range(9)]
#         self.nums = [int(i) for i in list(numbers.split(","))]
#         self.cage_size = []
#         self.cage_dict = {}  # 统计这个cage的大小
#         self.cage_sum = {}
#         self.complete = False # 是否可解
#         self.candidates = [0 for _ in range(81)] # 所有格子的候选数
#         self.lg = [0 for _ in range(1024)]
#         self.rowbit = [0 for _ in range(9)]
#         self.colbit = [0 for _ in range(9)]
#         self.block = [0 for _ in range(9)]

#         for i in range(9):
#             self.lg[ 1 << i ] = i + 1
#             self.block[i] = ((1 << 9) - 1) ^ self.block[i]
#             self.rowbit[i] = ((1 << 9) - 1) ^ self.rowbit[i]
#             self.colbit[i] = ((1 << 9) - 1) ^ self.colbit[i]
            

#         for _, pos in enumerate(cages):
#             if pos not in self.cage_dict:
#                 self.cage_dict[pos] = cages.count(pos)
#             if pos >= "A" and pos <= "Z":
#                 self.cage_sum[pos] = self.nums[ord(pos) - 65]
#             else:
#                 self.cage_sum[pos] = self.nums[ord(pos) - 97 + 26]
#         for i in range(81):
#             tmp_cands = list(set(sum( get_possible_candidates(self.cage_dict[self.cages[i]], self.cage_sum[self.cages[i]]), [] )))
#             for rdy in tmp_cands:
#                 self.candidates[i] |= (1 << (rdy - 1))
#             print(len(tmp_cands))
#         # for key in self.cage_dict:
#         #     print(f"{key}:{self.cage_dict[key]}")


#     def lowbit(self, x):
#         return x & (-x)

#     def getblk(self, x, y):
#         return (x // 3) * 3 + y // 3

#     def DFS(self, idx):
#         if idx == 81:
#             # print(self.candidates[6])
#             self.complete = True
#             return
        
#         else:
#             row = idx // 9
#             col = idx  % 9
#             tmp__ = self.candidates[idx]
#             while self.candidates[idx]  :
#                 number = self.lowbit(self.candidates[idx])
#                 self.candidates[idx] ^= number
#                 number = self.lg[number]
#                 self.cage_dict[self.cages[idx]] -= 1
#                 self.cage_sum[self.cages[idx]] -= number
#                 # print(f"{row} | {col}: {bin(self.candidates[idx])}:{number}:{self.cage_dict[self.cages[idx]]}")
#                 print(f"{row} | {col}: :{number}")
                

#                 if not ( (self.rowbit[row] >> (number - 1) )& 1 and  (self.colbit[col] >> (number - 1) )&1  and (self.block[self.getblk(row, col)] >> (number - 1) ) & 1):
#                     # print("OO")
#                     self.cage_sum[self.cages[idx]] += number
#                     self.cage_dict[self.cages[idx]] += 1
#                     continue

#                 elif self.cage_sum[self.cages[idx]] != 0 and self.cage_dict[self.cages[idx]] == 0:
#                     self.cage_sum[self.cages[idx]] += number
#                     self.cage_dict[self.cages[idx]] += 1
#                     continue

#                 elif self.cage_sum[self.cages[idx]] == 0 and self.cage_dict[self.cages[idx]] != 0:
#                     self.cage_sum[self.cages[idx]] += number
#                     self.cage_dict[self.cages[idx]] += 1
#                     continue
                
#                 self.grid[row][col] = number
#                 self.block[self.getblk(row, col)] ^= (1 << (number - 1))
#                 self.rowbit[row] ^= (1 << (number - 1))
#                 self.colbit[col] ^= (1 << (number - 1))
            
#                 self.DFS(idx + 1)
    

#                 if not self.complete:
#                     self.grid[row][col] = 0
#                     self.block[self.getblk(row, col)] ^= ( 1 << ( number - 1 ))
#                     self.rowbit[row] ^= (1 << ( number - 1))
#                     self.colbit[col] ^= (1 << ( number - 1))
#                     self.cage_sum[self.cages[idx]] += number
#                     self.cage_dict[self.cages[idx]] += 1 
#                     # self.candidates[idx] = tmp__
#                 else:
#                     break
#                 # self.
#             self.candidates[idx] = tmp__

#     def solve(self):
#         self.DFS(0)
    

# https://github.com/emiraga/varioku-js/tree/part3
    
        

        
if __name__ == "__main__":
    grids = "ABCCDDEEEABBFGHHIIABBFGGJKILLMNNJJKOPPMQRSSOOTQQQRUSOVTTWWUUUVVXYYYYZZZZXaabbbccZ"
    sums_ = "15,24,11,5,16,17,14,10,10,21,7,15,9,10,20,10,12,15,15,17,16,18,8,10,13,32,12,13,10"
    ksolver = killer_dfs_solver(grids, sums_)
    # ksolver.solve()
    
    res = Lst2Str(ksolver.grid)
    cmd_Visualization(res)  
    # diagnoal_1 = "000120040204000000003040060500000100000070000002000008010090800000000506070016000"
    # diagnoal_2 = "050300260083072014002000800300000000000201000000000002007000100230180470041009050"
    # test = Str2Lst(diagnoal_2)
    # test2 = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
    # t = std_dfs_solver(test2)
    # t.solve()
    # diagnoal_constraints_1 = {

    #         "0":set([(3,0),(2, 1),(1, 2),(0, 3)]),
    #         "1":set([(4,0),(3, 1),(2, 2),(1, 3), (0, 4)]),
    #         "2":set([(0,4),(1, 5),(2, 6),(3, 7), (4, 8)]),
    #         "3":set([(0,5),(1, 6),(2, 7),(3, 8)]),
    #         "4":set([(4,8),(5, 7),(6, 6),(7, 5), (8, 4)]),
    #         "5":set([(5,8),(6, 7),(7, 6),(8, 5)]),
    #         "6":set([(8,4),(7, 3),(6, 2),(5, 1), (4, 0)]),
    #         "7":set([(8,3),(7, 2),(6, 1),(5, 0)]),
    # }
    
    # # 135度中间对角线
    # diagnoal_constraints_2 = {
    #     "0":set([(i, i + 5) for i in range(4)]),
    #     "1":set([(i, i + 4) for i in range(5)]),
    #     "2":set([(i, i + 3) for i in range(6)]),
    #     "3":set([(i, i + 2) for i in range(7)]),
    #     "4":set([(i, i + 1) for i in range(8)]),
    #     "5":set([(i, i) for i in range(9)]),
    #     "6":set([(i + 1, i) for i in range(8)]),
    #     "7":set([(i + 2, i) for i in range(6)]),
    #     "8":set([(i + 3, i) for i in range(5)]),
    #     "9":set([(i + 4, i) for i in range(4)]),
    #     "10":set([(i + 5, i) for i in range(3)]),
    # }

    # arr = "000006000907080016001300800200900000000053000000400000790014000350847020000100000"
    # regions =  "ABBBBBBCDAABBBCCCDAAACCCDDDAEACCFFDGAEEFFFDDGEEFFFFDHGEEHHHHHHGEEIHIIHGGIIIIIIGGG"
    # jigsaw_test = jigsaw_dfs_solver(arr, regions)
    # jigsaw_test.solve()
    # res = Lst2Str(jigsaw_test.grid)
    # cmd_Visualization(res)
    