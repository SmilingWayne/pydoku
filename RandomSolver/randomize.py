import numpy
import random
import time
from random import randint
# import sys
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

da3 =[0]*3
da33 =[0]*3
remainder =[0]*10
divider =[0]*10
closebythree =[0]*10
closebythree_plus3=[0]*10
modeclose_bythree=[0]*10
backword =[0]*10

for i in range(0,3):
    da3[i]=i*3
    da33[i]=da3[i]+3
    
for p in range(0,10):
    backword[p]=9-p
    remainder[p]=p%3
    divider[p]=p//3
    closebythree[p]=p//3*3
    closebythree_plus3[p]=closebythree[p]+3
    modeclose_bythree[p]=p%3*3
    
def clear_point(sudo,trnum,x,y):

    for v in range(0,9):
        sudo[trnum][v][y]=0
        sudo[trnum][x][v]=0
        sudo[v+1][x][y]=0
    
    
    for r in range(0,9):
        sudo[trnum][r//3+x-x%3][r%3+y-y%3]=0 

def clear_bits(save):

    for i in range(0,9):
        for j in range(0,9):
            for p in range(0,10):
                save[p][i][j]=0 
        
    


def isthesame(sudo,sudoext):

    for i in range(0,9):
        for k in range(0,9):
            if(sudo[i][k]!=sudoext[i][k]):
                return 0 
        
    return 1 


def copysudo(sudo,sudoext):

    for i in range(0,9):
        for k in range(0,9):
            sudo[i][k]=sudoext[i][k] 
        
    return  

def bitcopysudo(sudo,sudoext):

    for p in range(0,10):
        for i in range(0,9):
            for k in range(0,9):
                sudo[p][i][k]=sudoext[p][i][k]
            

def canputin(sudo,x,y,z):

    if(sudo[x][y]!=0):
        return -1 

    for a in range(0,9):
    
        if(sudo[a][y]==z):
            return -1 
    
    
    for b in range(0,9):
    
        if(sudo[x][b]==z):
            return -1 
    
    
    for a in range(x//3*3,x//3*3+3):
        for b in range(y//3*3,y//3*3+3):
        
            if(sudo[a][b]==z):
                return -1 
            
            
        
    
    return 1 
    

def sumlay(lay,q,p):

    for x in range(q*3,q*3+3):
        for y in range(p*3,p*3+3):
        
            if(lay[x][y]==False):
                return 0 
        
    return 9 

def isexist(sudo,x, y, z):

    for a in range(x//3*3,x//3*3+3):
        for b in range(y//3*3,y//3*3+3):
        
            if(sudo[a][b]==z):
                return -1 
        
    
    return 1 



def change_bit(sudo):

    con=0
    py=0
    al=0
    
    for si in range(0,9):
        for sk in range(0,9):
        
            i=si 
            k=sk 
            
            if(sudo[0][i][k]!=0):
                continue 
            
            for l in range(1,10):
                if(sudo[l][i][k]==1):
                    if(con==1):
                        con=0 
                        break 
                    else:
                        con=1 
                        py=l 
                    
                
            
            if(con==1):
                sudo[0][i][k]=py 
                for v in range(0,9):
                    sudo[py][v][k]=0 
                    sudo[py][i][v]=0 
                    sudo[py][divider[v]+closebythree[i]][remainder[v]+closebythree[k]]=0 
                
                al=1 
                con=0 
            
        
    
    return al 


def square_bit (sudo):

    label=0
    block=[0]*10 

    for a in range(0,3):
        for b in range(0,3):
        
            for i in range(da3[a],da33[a]):
                for k in range(da3[b],da33[b]):
                
                    if(sudo[0][i][k]!=0):
                        continue 
                    for p in range(1,10):
                        block[p]+=sudo[p][i][k] 
                
            
            for p in range(1,10):
                if(block[p]==1):
                    for r in range(0,9):
                        i=divider[r]+da3[a]
                        k=remainder[r]+da3[b]
                        if(sudo[p][i][k]==1):
                        
                            sudo[0][i][k]=p 
                            
                            for u in range(1,10):
                                sudo[u][i][k]=0 
                            
                            for v in range(0,9):
                                sudo[p][v][k]=0 
                                sudo[p][i][v]=0 
                            
                            label=1 
                block[p]=0 
    return label 


def row_bit (sudo):

    changeor=0
    row=[0]*10
    for si in range(0,9):
    
        i=si 
        for sk in range(0,9):
        
            if(sudo[0][i][sk]!=0):
                continue 
            
            for p in range(1,10):
                row[p]+=sudo[p][i][sk] 
        
        for p in range(1,10):
        
            if(row[p]==1):
            
                for k in range(0,9):
                
                    if(sudo[p][i][k]==1):
                    
                        sudo[0][i][k]=p 
                        for r in range(0,9):
                            sudo[r+1][i][k]=0 
                            sudo[p][r][k]=0 
                            sudo[p][divider[r]+closebythree[i]][remainder[r]+closebythree[k]]=0 
                        changeor=1 

            row[p]=0 

    return changeor 

def col_bit(sudo):

    changeor=0
    col=[0]*10
    colnum=[0]*10
    for sk in range(0,9):
    
        k=sk 
        for si in range(0,9):
        
            if(sudo[0][si][k]!=0):
                continue 
            
            for p in range(1,10):
            
                if(sudo[p][si][k]==1):
                
                    col[p]+=1 
                    colnum[p]=si 
                
            
        
        for p in range(1,10):
        
            if(col[p]==1):
            
                sudo[0][colnum[p]][k]=p 
                
                for u in range(0,9):
                    sudo[p][colnum[p]][u]=0 
                    sudo[p][divider[u]+closebythree[colnum[p]]][remainder[u]+closebythree[k]]=0 
                    sudo[u+1][colnum[p]][k]=0 
                
                changeor=1 
            
            col[p]=0 
        
    
    
    return changeor 


def presolvesudo(sudo):

    lok=change_bit(sudo)
    
    while(square_bit(sudo)==1 or col_bit(sudo)==1 or row_bit(sudo)==1):
    
        change_bit(sudo)
        lok=1
    
    return lok

    
def build_bit(sudo):


    for f in range(0,10):
        for i in range(0,9):
            for k in range(0,9):
                if(sudo[0][i][k]==0):
                
                    if(canputin(sudo[0],i,k,f)==1):
                        sudo[f][i][k]=1 
                
    presolvesudo(sudo) 
    
    return 1 

def low_build_bit(sudo):

    for f in range(0,10):
        for i in range(0,9):

            for k in range(0,9):
            
                if(sudo[0][i][k]==0):
                
                    if(canputin(sudo[0],i,k,f)==1):
                        sudo[f][i][k]=1 

    return 1 


def linecheck(tempsudo):

    for p in range(1,10):
        for i in range(0,9):
    
            for k in range(0,9):
            
                if(tempsudo[0][i][k]==p):
                    break 
                if(tempsudo[p][i][k]==1):
                    break 
                if(k==8):
                    return 0 
            
        
    for p in range(1,10):
        for i in range(0,9):
            for k in range(0,9):
            
                if(tempsudo[0][k][i]==p):
                    break 
                if(tempsudo[p][k][i]==1):
                    break 
                if(k==8):
                    return 0 
            
        
    for p in range(1,10):
        for i in range(0,9):
            for k in range(0,9):
            
                if(tempsudo[0][i-i%3+k//3][i%3*3+k%3]==p):
                    break 
                if(tempsudo[p][i-i%3+k//3][i%3*3+k%3]==1):
                    break 
                if(k==8):
                    return 0 
            
        
    
    for i in range(0,9):
    
        for k in range(0,9):
        
            for p in range(0,10):
            
                if(tempsudo[p][i][k]!=0):
                    break 
                if(p==9):
                    return 0 
            
        
    
    
    return 1 

def isvacant(sudo):

    for i in range(0,9):
        for k in range(0,9):
        
            if(sudo[i][k]==0):
                return 1 
        
    return 0 

def isok(sudo):

    mul=0 
    sum=0 
    
    for i in range(0,9):
    
        sum=0 
        mul=1 
        for k in range(0,9):
        
            sum+=sudo[i][k] 
            mul*=sudo[i][k] 
        
        if(sum!=45 or mul!=362880):
            return -1 
    
    
    for k in range(0,9):
    
        sum=0 
        mul=1 
        for i in range(0,9):
        
            sum+=sudo[i][k] 
            mul*=sudo[i][k] 
        
        if(sum!=45 or mul!=362880):
            return -1 
    
    return 1 

def check(sudo,sudoext):

    for i in range(0,9):
        for k in range(0,9):
        
            if(sudoext[i][k]!=0):
                if(sudo[i][k]!=sudoext[i][k]):
                    return -1 
        
    return 1 


@runtime_display
def solvesudo(sudo,sudoext):


    lay = [[0]*9 for _ in range(0,9)] 
    backer=0 
    dt=0 
    
    sudop= [[[0]*9 for _ in range(0,9)] for _ in range(0,10)] 
    copysudo(sudop[0],sudoext) 
    build_bit(sudop) 
    
    if(isvacant(sudop[0])==0):
    
        copysudo(sudo[0],sudop[0]) 
        return 
    
    
    havetry=[0]*10 
    first_start=True
    #print(sudop[0])
    while (first_start==True or (backer==2 or isok(sudo[0])==-1 or check(sudo[0],sudoext)==-1)):
        first_start=False
        dt=0 
        backer=0 
        for i in range(0,10):
            havetry[i]=0 
        
        bitcopysudo(sudo,sudop) 
        
        for dt in range(1,9):# fill num 1-9 
            

            trnum=randint(1,9) 
            while (havetry[trnum]==1): 
                trnum=randint(1,9) 
            
            havetry[trnum]=1 
            # dt++ 
            
            if(dt>=2):
                if(linecheck(sudo)==0):
                    backer=2 
                    break 
                
            if(dt>=2):
                if(isvacant(sudo[0])==0):
                    break 
                
            for ii in range(0,9):
                for kk in range(0,9):
                    lay[ii][kk]=0 
            
            for b in range(0,9):
            
                p=b//3 
                q=b%3 
                
                if(isexist(sudo[0],q*3,p*3,trnum)==-1):
                    continue  
                
                
                x=randint(0,2)+q*3 
                y=randint(0,2)+p*3 
                lay[x][y]=1 
                rng=sudo[trnum][x][y] 
        
                while(rng!=1):
                    x=randint(0,2)+q*3 
                    y=randint(0,2)+p*3 
                    if(lay[x][y]==1):
                        continue 
                    lay[x][y]=1 
                    if(sumlay(lay,q,p)==9):
                        break 
                    rng=sudo[trnum][x][y] 
                if(sudo[0][x][y]==0):
                    sudo[0][x][y]=trnum 
                    clear_point(sudo,trnum,x,y) 
                    presolvesudo(sudo) 
                    #presolvesudo(sudo) 
                else:
                    backer=2 
                    break 




def sudoku_solver(puzzle):
    inputer = ''
    for i in range(0,9):
        for j in puzzle[i]:
            inputer += str(j)
    sudoans = [[[0]*9 for _ in range(0,9)] for _ in range(0,10)] 
    sudoin = [[0]*9 for _ in range(0,9)] 

    for i in range(0,9):
        for j in range(0,9):
            sudoin[i][j]=ord(inputer[i*9+j])-ord('0')

    solvesudo(sudoans,sudoin)
    solution = []
    for i in range(0,9):
        solution.append(sudoans[0][i])
    return solution



Questions = [                         "500000300020100070008000009040007000000821000000600010300000800060004020009000005",
                         "800000009040001030007000600000023000050904020000105000006000700010300040900000008",
                         "000070100000008050020900003530000000062000004094600000000001800300200009000050070",
                         "000006080000100200009030005040070003000008010000200600071090000590000004804000000",
                         "000056000050109000000020040090040070006000300800000002300000008002000600070500010",
                         "500000004080006090001000200070308000000050000000790030002000100060900080400000005",
                         "070200009003060000400008000020900010800004000006030000000000600090000051000700002",
                         "100080000005900000070002000009500040800010000060007200000000710000004603030000402",
                         "000900100000080007004002050200005040000100900000070008605000030300006000070000006",
                         "000001080030500200000040006200300500000008010000060004050000700300970000062000000",
                         "800000005040003020007000100000004000090702060000639000001000700030200040500000008",
                         "900000001030004070006000200050302000000060000000078050002000600040700030100000009",
                         "500000008030007040001000900020603000000725000000800060009000100070400030800000005",
                         "400000009070008030006000100050702000000065000000003020001000600080300070900000004",
                         "100006009007080030000200400000500070300001002000090600060003050004000000900020001",
                         "800000001050009040003000600070056000000980000000704020006000300090400050100000008",
                         "010000009005080700300700060004250000000000000000840200008007500600000030090000001",
                         "300000005020007040001000900080036000000028000000704060009000100070400020500000003",
                         "400000003080002060007000900010508000000701000000026050009000700020600080300000004"]
    
    # grid_str = "100006009007080030000200400000500070300001002000090600060003050004000000900020001"
for grid_str in Questions:
    sudoans = [[[0]*9 for _ in range(0,9)] for _ in range(0,10)] 
    sudoin = [[0]*9 for _ in range(0,9)] 

    for i in range(0,9):
        for j in range(0,9):
            sudoin[i][j]=ord(grid_str[i*9+j])-ord('0')
    solvesudo(sudoans,sudoin)

#print(sudoin)



        


# for i in range(0,9):
#     for j in range(0,9):
#         print(sudoans[0][i][j],end='')

#     print("")