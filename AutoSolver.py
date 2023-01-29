from DFSsolver import std_dfs_solver
from Utils import *
import pyautogui as pg
# 250300000000946000010500000005000096600000000900030040087000200000004300000070005
if __name__ == '__main__':
    t = input("Input:")
    solver_ = std_dfs_solver(t) # 解数独的函数
    solver_.solve()
    res = Lst2Str(solver_.grid) # 结果转换为字符串输出
    print(res)
    time.sleep(3)
    for index, num in enumerate(res):
        pg.press(num)
        pg.hotkey('right')    
        if (index + 1) % 9 == 0:
            pg.hotkey('down')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')


