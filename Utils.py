import time

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



def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    with open(filename) as f:
        return f.read().strip().split(sep)
    
if __name__ == '__main__':
    test = "004700020200008000000260010000900102100000005709003000030054000000800003020007800"
    print(cmd_Visualization(test))
