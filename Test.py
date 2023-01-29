sudoku = [[0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0]]

conditions = [[[0,0,1,0],9],
              [[0,1,0,2],8],
              [[0,3,0,4,0,5,1,5,2,5],17],
              [[1,1,2,0,2,1],11],
              [[1,2,1,3,2,2,2,3],11],
              [[1,4,2,4,3,3,3,4],14],
              [[3,0,3,1,4,0,4,1,5,0],17],
              [[3,2,4,2,5,1,5,2],14],
              [[3,5,4,5,5,5],8],
              [[4,3,5,3],10],
              [[4,4,5,4],7]]

def checkConditions():
    
    for c in conditions:
        l = len(c[0])
        arr = []

        while l!=0 :
            arr.append(sudoku[c[0][l-2]][c[0][l-1]])
            l = l-2

        if arr.count(0) > 0:
            continue

        elif sum(arr) != c[1]:
            return False

    return True

def printSudoku():

    for i in sudoku:
        for j in i:
            print("\t"+str(j),end="")
        print("\n")

    print("\n")

def checkSudoku(row,column,num):

    for x in range(6):
        if sudoku[row][x]==num:
            return False

    for x in range(6):
        if sudoku[x][column]==num:
            return False

    startRow = row - row%2
    startColumn = column - column%3
    for i in range(2):
        for j in range(3):
            if sudoku[i+startRow][j+startColumn]==num:
                return False

    return True

def solSudoku(row,column):

    if row==5 and column==6:
        return True

    if column==6:
        row+=1
        column=0

    if sudoku[row][column]>0:
        return solSudoku(row,column+1)

    for num in range(6):
        if checkSudoku(row,column,num+1) and checkConditions():
            sudoku[row][column]=num+1
            if solSudoku(row,column+1):
                return True
        sudoku[row][column]=0

    return False

printSudoku()
solSudoku(0,0)
print("\n\nAfter Solution - \n")
printSudoku()