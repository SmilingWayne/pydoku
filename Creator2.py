import copy
import random

from Utils import runtime_display, cmd_Visualization
class Sudoku:
    # @param board, a 9x9 2D array
    # Solve the Sudoku by modifying the input board in-place.
    # Do not return any value.
    def __init__(self):
        self.grids = [(i,j) for j in range(9) for i in range(9)]
        self.peercross = [[[[(j,i) for i in range(9)],[(i,k) for i in range(9)],[(j - j % 3 + i // 3,k - k % 3 + i % 3)for i in range(9)]] for k in range(9)]for j in range(9)]
        self.peers = [[set(sum(self.peercross[j][k],[])) - set([(j,k)]) for k in range(9)] for j in range(9)]
        self.finalsolution = False

    @runtime_display
    def solveSudoku(self, board):
        self.finalsolution = False
        possiblenumbers = [[[i for i in range(1,10)]for j in range(9) ]for k in range(9)]
        assert (len(board) == 9 and all((len(board[i]) == 9) for i in range(9))) == True
        if not self.preProcess(board,possiblenumbers):return False
        self.reSlove(possiblenumbers,1)
        return self.finalsolution
    def preProcess(self,board,possiblenumbers):
        for i in range(81):
            if not self.fill(i // 9,i % 9,board[i // 9][i % 9],possiblenumbers):
                return False
        return True
    #@return whether the value can be filled in the current grid
    def fill(self,x,y,value,possiblenumbers):
        if value not in range(1,10) and value not in "123456789":return True
        if int(value) not in possiblenumbers[x][y] or x not in range(9) or y not in range(9):return False
        if len(possiblenumbers[x][y]) == 1 or all([self.eliminate(x,y,i,possiblenumbers) for i in  [j for j in possiblenumbers[x][y] if j != int(value)]]):
            return True
        return False
    #@return whether elimatesuccess or not
    def eliminate(self,x,y,value,possiblenumbers):
        if value not in possiblenumbers[x][y]:
            return True
        if len(possiblenumbers[x][y]) == 1:
            return False
        possiblenumbers[x][y].remove(value)
        #stg1
        if len(possiblenumbers[x][y]) == 0 or len(possiblenumbers[x][y]) == 1 and  not all([self.eliminate(i,j,possiblenumbers[x][y][0],possiblenumbers) for (i,j) in self.peers[x][y] if (possiblenumbers[x][y][0]) in possiblenumbers[i][j]]):
             return False
        #stg2
        for k in self.peercross[x][y]:
            tem = [(i,j) for (i,j) in k if value in possiblenumbers[i][j]]
            if len(tem) == 1 and len(possiblenumbers[tem[0][0]][tem[0][1]]) > 1 and  not self.fill(tem[0][0],tem[0][1],value,possiblenumbers):
                return False
        return True
    def reSlove(self,possiblenumbers,deepth):
        if all(len(possiblenumbers[i][j]) == 1 for (i,j) in self.grids):
            if not self.finalsolution:
                self.finalsolution = copy.deepcopy(possiblenumbers)
            else:
                self.finalsolution = True
            return
        length,x,y = min((len(possiblenumbers[i][j]),i,j) for (i,j) in self.grids if len(possiblenumbers[i][j]) > 1)
        posibility = copy.copy(possiblenumbers[x][y])
        for i in posibility:
            copyindex = copy.deepcopy(possiblenumbers)
            if self.fill(x,y,i,copyindex) and self.finalsolution != True:
                self.reSlove(copyindex,deepth + 1)
        return
    @runtime_display
    def generateSolvedSudo(self):
        self.finalsolution = False
        possiblenumbers = [[[i for i in range(1,10)]for j in range(9) ]for k in range(9)]
        self.reGenerate(possiblenumbers)
        return [[str(self.finalsolution[i][j][0]) for j in range(9)] for i in range(9)]
    def reGenerate(self,possiblenumbers):
         if all(len(possiblenumbers[i][j]) == 1 for (i,j) in self.grids):
            self.finalsolution = copy.deepcopy(possiblenumbers)
            return True
         length,x,y = random.choice([(len(possiblenumbers[i][j]),i,j) for (i,j) in self.grids if len(possiblenumbers[i][j]) == (min(len(possiblenumbers[x][y]) for (x,y) in self.grids if len(possiblenumbers[x][y]) > 1))])
         posibility = copy.copy(possiblenumbers[x][y])
         for i in posibility:
            copyindex = copy.deepcopy(possiblenumbers)
            if self.fill(x,y,i,copyindex) and self.finalsolution != True:
                if self.reGenerate(copyindex):
                    return True
         return False
    #The most simple way to generate a puzzle
    def generateUnsolvedPuzzle(self):
        solvedPuzzle = self.generateSolvedSudo()
        ran = copy.deepcopy(self.grids)
        random.shuffle(ran)
        for (i,j) in ran:
            buffer = solvedPuzzle[i][j]
            solvedPuzzle[i][j] = '.'
            if self.solveSudoku(solvedPuzzle) == True:
                solvedPuzzle[i][j] = buffer
        return [''.join(i) for i in solvedPuzzle]
    #a little complicated way to generate a symetry sudoky puzzle
    @runtime_display
    def generateCentralSymmetryPuzzle(self):
        solvedPuzzle = self.generateSolvedSudo()
        ran = copy.deepcopy([self.grids[i] for i in range(len(self.grids) // 2 + 1)])
        random.shuffle(ran)
        for (i,j) in ran:
            buffer1 = solvedPuzzle[i][j]
            buffer2 = solvedPuzzle[8 - i][8 - j]
            solvedPuzzle[i][j] = '.'
            solvedPuzzle[8 - i][8 - j] =  '.'
            if self.solveSudoku(solvedPuzzle) == True:
                solvedPuzzle[i][j] = buffer1
                solvedPuzzle[8 - i][8 - j] = buffer2
        return [''.join(i) for i in solvedPuzzle]
    #show the puzzle
    def show(self,puzzle):
        final_ans = "".join([ puzzle[i][j] for i in range(9) for j in range(9)])
        cmd_Visualization(final_ans)
        # for i in range(len(puzzle)):
        #     for j in  range(len(puzzle[i])):
        #         print(puzzle[i][j] + " ")
        #         # if puzzle[i][j] is chr:
        #         #     print(puzzle[i][j])
        #         # else:
        #         #     print(puzzle[i][j][0])
        #         if j == 2 or j == 5:
        #             print ('|')
            
        #     if i == 2 or i == 5:
        #         print( '-' * 29)
        
s = Sudoku()
print('------------answer-----------')
s.solveSudoku(["8........", "..36.....", ".7..9.2..", ".5...7...", 
"....457.." ,"...1...3.", "..1....68", "..85...1.", ".9....4.."])

# #print  s.solveSudoku(['.7.8....2', '.6.9...3.', '.......47', '....1..89', '.8.4.....', '.....2...', '7.93.....', '1...75.9.', '3.......1'])
# puzzle = s.generateCentralSymmetryPuzzle()
puzzle = s.generateSolvedSudo()
s.show(puzzle)
# s.show(s.solveSudoku(puzzle))