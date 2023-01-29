import numpy as np
import time


def get_possible_candidates(size_, value_):
    """ 一个大小为size_的cage 和为value_
        返回所有的情况
        仅支持九宫格数独
    Args:
        size_ (_int_): size of the cage
        value_ (_int_): sum of the cage

    Returns:
        _type_: [[idxs of number],[]]
    """
    ref = [i for i in range(1,10)]
    res = []
    def backTrace(idx, path, size_, value_):
        if len(path) == size_ and value_ == 0:
            res.append(path[:])
            return
        if value_ < 0 or len(path) > size_:
            return
        for i in range(idx,len(ref)):
            path.append(ref[i])
            backTrace(i + 1, path, size_, value_ - ref[i]) # i + 1
            path.pop()

    backTrace(0, [], size_ , value_)
    return res

def Str2Lst(string):
    """_summary_
        字符串化为列表
        加入可行性检查
    """

    if not isinstance(string, str):
        raise ValueError("Not a String, CHECK it again!")

    if len(string) != 81:
        raise ValueError("Input length != 81, CHECK it again!")
        
    if "." in string:
        string.replace(".", "0")

    return [[int(num) for num in string[i : i + 9]] for i in range(0, 81, 9)]

    

def Lst2Str(lst):
    """_summary_
        数独列表转化为字符串
        加入可行性检查
    """

    if isinstance(lst, str) :
        if len(lst) == 81:
            return lst
        else:
            raise ValueError("Input length != 81, CHECK it again!") 

    elif isinstance(lst, list):
        dimension = np.array(lst).ndim
        if dimension == 1 :
            return "".join([str(i) for i in lst])
        elif dimension == 2:
            return "".join(["".join([str(k) for k in i]) for i in lst])
        else:
            raise ValueError("Input dimension > 2, CHECK it again!")

    else:
        raise ValueError("Input is not a String or List! CHECK it again!")


def cmd_Visualization(grid_str):

    """可读性提升"""
    print('')
    grid = list(grid_str)
    row = list('+-------+-------+-------+')
    for index, chr in enumerate(grid):
        if index % 9 == 0:
            print(''.join(row))
            if index % 27 == 0 and index > 0:
                print('+-------+-------+-------+')
            row = []
        if index % 3 == 0:
            row.extend(['|', ' '])
        row.extend([chr, ' '])
        if (index + 1) % 9 == 0:
            row.append('|')
        if index == len(grid_str) - 1:
            print(''.join(row))
            print('+-------+-------+-------+\n')

def runtime_display(func):
    """_summary_
        Calculate running time

    Args:
        func (_function_): _The function you wanna cal running time_
    """
    def wrapper(*args):
        t1 = time.time()
        result = func(*args)
        t2 = time.time()
        print("Total time: {:.4} s".format(t2 - t1))
        return result
    return wrapper

if __name__ == '__main__':
    test = "004700020200008000000260010000900102100000005709003000030054000000800003020007800"
    print(cmd_Visualization(test))

