import random
import numpy as np
import copy
from Utils import *


def all_candidates(arr):
    """_summary_
        Prepare all candidates for Arr ipt
    Args:
        arr (_type_): _description_

    Returns:
        _type_: _description_
    """
    candidates = np.zeros(shape = (9,9,9), dtype = bool)
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(len(arr)):
        if arr[i] != '0':
            x_ = i // 9
            y_ = i % 9
            ipt = ord(arr[i]) - 49
            grid[x_][y_] = ipt
            candidates[ipt, x_, :] = True
            candidates[ipt, :, y_] = True
            candidates[ipt, (x_//3) * 3: (x_//3) * 3 + 3, (y_ // 3) * 3: (y_ // 3) * 3 + 3] = True
            candidates[:, x_, y_] = True
    
    # for i in range(9):
    #     for j in range(9):
    #         print(f"{i}-{j}")
    #         print(np.where(candidates[:, i ,j] == False)[0] + 1)
            # pass
    return candidates


@runtime_display
def randomdize():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    arr = [i for i in range(1, 10)]
    colbit = [0 for _ in range(9)]
    block = [0 for _ in range(9)]   
    for i in range(8):
        if i == 0:
            random.shuffle(arr)
            grid[i] = copy.deepcopy(arr)
            
            for idx in range(9):
                colbit[idx] |= (1 << (arr[idx] - 1) )
                block[idx // 3] |= (1 << (arr[idx] - 1) )
        else:
            Flag = True
            k = 0
            while Flag:
                for idx in range(9):
                    cur_blk = (i // 3) * 3 + idx // 3
                    if block[cur_blk] & (1 << (arr[idx] - 1)) \
                        or colbit[idx] & (1 << (arr[idx] - 1)) :
                        random.shuffle(arr)
                        k += 1
                        break
                    if idx == 8:
                        # print(f"Row{i} Takes {k} Rimes")
                        Flag = False
                                
            for idx in range(9):
                grid[i] = copy.deepcopy(arr)
                cur_blk = i // 3 * 3 + idx // 3
                block[cur_blk] ^= (1 << (arr[idx] - 1))
                colbit[idx] ^= (1 << (arr[idx] - 1))
            grid = np.array(grid)
    # print(np.sum(grid[0:9,:])
            grid[8, ] = 45 - np.sum(grid[0:8,:], axis = 0)  
    
    return grid


@runtime_display
def Get_Final_Grid():
    arr = np.arange(1,10,1)
    np.random.shuffle(arr)
    arr = np.concatenate((arr, arr), axis = 0)
    arr = np.concatenate((arr, arr), axis = 0)
    
    grid = np.zeros(shape=(9,9), dtype =int)
    grid[0, :] = arr[0:9]
    grid[1, :] = arr[3:12]
    grid[2, :] = arr[6:15]

    grid[3, :] = arr[7:16]
    grid[4, :] = arr[10:19]
    grid[5, :] = arr[13:22]

    grid[6, :] = arr[14:23]
    grid[7, :] = arr[17:26]
    grid[8, :] = arr[20:29]


    choices = np.random.randint(0, 47, 2000)
    for choice in choices:
        # print(choice)
    # ======================= UP: Generate Valid Grid =======================
    
        if choice == 0:
            # print("A")
        # 18个行/列变换方式
            grid[[1,2], :] = grid[[2,1], :]
        elif choice == 1:
            grid[[0,1], :] = grid[[1,0], :]
        elif choice == 2:
            grid[[0,2], :] = grid[[2,0], :]
        elif choice == 3:
            grid[[3,4], :] = grid[[4,3], :]
        elif choice == 4:
            grid[[3,5], :] = grid[[5,3], :]
        elif choice == 5:
            grid[[4,5], :] = grid[[5,4], :]
        elif choice == 6:
            grid[[6,7], :] = grid[[7,6], :]
        elif choice == 7:
            grid[[6,8], :] = grid[[8,6], :]
        elif choice == 8:
            grid[[7,8], :] = grid[[8,7], :]
        elif choice == 9:
            grid[:, [1,2]] = grid[:, [2,1]]
        elif choice == 10:
            grid[:, [0,1]] = grid[:, [1,0]]
        elif choice == 11:
            grid[:, [0,2]] = grid[:, [2,0]]
        elif choice == 12:
            grid[:, [3,4]] = grid[:, [4,3]]
        elif choice == 13:
            grid[:, [3,5]] = grid[:, [5,3]]
        elif choice == 14:
            grid[:, [4,5]] = grid[:, [5,4]]
        elif choice == 15:
            grid[:, [6,7]] = grid[:, [7,6]]
        elif choice == 16:
            grid[:, [6,8]] = grid[:, [8,6]]
        elif choice == 17:
            grid[:, [7,8]] = grid[:, [8,7]]
        # print(grid)
        # ======================= UP: In Blocks Row / Column Swap =======================
        elif choice == 18 or choice == 35 or choice == 36:
            grid[[0,1,2, 3,4,5], :] = grid[[3,4,5, 0,1,2], :]
        elif choice == 19 or choice == 37 or choice == 38:
            grid[[3,4,5, 6,7,8], :] = grid[[6,7,8, 3,4,5], :]
        elif choice == 21 or choice == 39 or choice == 40:
            grid[[0,1,2, 6,7,8], :] = grid[[6,7,8, 0,1,2], :]
        elif choice == 22 or choice == 41 or choice == 42:
            grid[:, [0,1,2, 3,4,5]] = grid[:, [3,4,5, 0,1,2]]
        elif choice == 23 or choice == 43 or choice == 44:
            grid[:, [0,1,2, 6,7,8]] = grid[:, [6,7,8, 0,1,2]]
        elif choice == 24 or choice == 45 or choice == 46:
            grid[:, [3,4,5, 6,7,8]] = grid[:, [6,7,8, 3,4,5]]

        # ======================= UP: 3 Rows / Columns Swap =======================
        
        elif choice == 25 or choice == 26 or choice == 27:
            grid = np.rot90(grid, 1)
        elif choice == 28 or choice == 29 or choice == 30:
            grid = np.rot90(grid, 2)


        # ======================= UP: Rotate Grid =======================
        elif choice == 31 or choice == 32:
            flag_1 = np.random.randint(low = 1, high = 10, size = 2)
            while flag_1[0] == flag_1[1]:
                flag_1 = np.random.randint(low = 1, high = 10, size = 2)
            ori_ = np.where(grid == flag_1[0])
            to_ = np.where(grid == flag_1[1])
            grid[ori_] = flag_1[1]
            grid[to_] = flag_1[0]


        # ======================= UP: Swap 2 Nums =======================
        elif choice == 33 or choice == 34:
            grid = grid.T

        # ======================= UP: Flip =======================
        

    return grid
    
if __name__ == "__main__":
    # all_candidates("002400006030010000500008000007000002010000030900600400000007001000090080400200500")
    print(Get_Final_Grid())
    print(randomdize())


        


    # 0 1 2 3 4 5 6 7 8 

    # 就是可以讲现在这个金融市场，情况很复杂很多变！# 控制变量了！有一个标准/科学方法/量化标准！