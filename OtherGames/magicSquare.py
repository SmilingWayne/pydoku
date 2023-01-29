#利用numpy模块构造幻方
import numpy as np
 
#列表循环左移offset位
def left_shift(lst, offset):
    return [lst[(i+offset)%len(lst)] for i in range(len(lst))]
 
#列表循环右移offset位
def right_shift(lst, offset):
    return [lst[i-offset] for i in range(len(lst))]
 
#构造奇数阶幻方
def magic_of_odd_order(n):
    p = (n-1)//2
 
    #创建矩阵1
    initial_lst1 = list(range(p+1,n))+list(range(p+1))
    initial_mat1 = []
    for i in range(n):
        initial_mat1.append(left_shift(initial_lst1, i))
    mat1 = np.array(initial_mat1)
 
    #创建矩阵2
    initial_lst2 = list(range(p,-1,-1))+list(range(2*p,p,-1))
    initial_mat2 = []
    for i in range(n):
        initial_mat2.append(right_shift(initial_lst2, i))
    mat2 = np.array(initial_mat2)
 
    #创建矩阵3,即元素全为1的矩阵
    mat3= np.ones((n,n),dtype=np.int64)
 
    #构造幻方
    magic = n*mat2 + mat1 + mat3
    return magic
 
#构造4n阶幻方函数
def magic_of_4n_order(n):
    mat = np.array(range(1,n*n+1)).reshape(n,n)
    for i in range(n//4):
        for j in range(n//4):
            for k in range(4): 
                #将每个4*4小方块的对角线换成互补元素
                mat[k+4*j][k+4*i] = n*n+1-mat[k+4*j][k+4*i]
                mat[k+4*j][3-k+4*i] = n*n+1-mat[k+4*j][3-k+4*i]
 
    return mat
 
#构造4n+2阶幻方函数
def magic_of_4n2_order(n):
    p = (int)(n/2)
    matA = magic_of_odd_order(p)
    matD = matA+p**2
    matB = matD+p**2
    matC = matB+p**2
 
    #交换矩阵块A与矩阵块C中特定元素的位置
    row = (int)((p-1)/2)
    for i in range(p):
        if i != row:
            for k in range((int)((n-2)/4)):
                matA[i][k],matC[i][k] = matC[i][k],matA[i][k]
        else:
            for k in range((int)((n-2)/4)):
                matA[i][row+k],matC[i][row+k] = matC[i][row+k],matA[i][row+k]
 
    #交换矩阵块B与矩阵块D中特定元素的位置
    col = (int)((p-1)/2)
    for j in range(col+2-(int)((n-2)/4),col+1):
        for i in range(p):
            matB[i][j],matD[i][j] = matD[i][j],matB[i][j]
 
    #合并矩阵块A,B,C,D组成幻方
    magic = np.row_stack((np.column_stack((matA,matB)),np.column_stack((matC,matD))))
    return magic


def run(N):
    magic = None
    if N <= 1:
        print("Invalid.")
        return -1
    elif N % 4 == 0:
        magic = magic_of_4n_order(N)
    elif N % 2 == 0:
        magic = magic_of_4n2_order(N)
    else:
        magic = magic_of_odd_order(N)
    return magic
if __name__ == "__main__":
    Number = 6                      # 12, 7
    result = run(Number)
    print(result)
    np.savetxt(f"../../Data/Result{Number}.csv", result, delimiter=",")


