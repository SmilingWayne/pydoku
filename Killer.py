import copy,sys

rulesFile="rules.csv"

sudo=[]
manuRules=[]
manuRulesSum=[]
sumDict={
    3:[1,2],
    4:[1,3],
    5:[1,4,2,3],
    6:[1,5,2,4],
    7:[1,6,2,5,3,4],
    8:[1,7,2,6,3,5],
    9: [1,8,2,7,3,6,4,5],
    10:[1,9,2,8,3,7,4,6],
    11:[2,9,3,8,4,7,5,6],
    12:[3,9,4,8,5,7],
    13:[4,9,5,8,6,7],
    14:[5,9,6,8],
    15:[6,9,7,8],
    16:[7,9],
    17:[8,9]
}
sumDictDup={
    3:[1,2],
    4:[1,2,3],
    5:[1,4,2,3],
    6:[1,5,3,2,4],
    7:[1,6,2,5,3,4],
    8:[1,7,2,4,6,3,5],
    9: [1,8,2,7,3,6,4,5],
    10:[1,9,2,8,5,3,7,4,6],
    11:[2,9,3,8,4,7,5,6],
    12:[3,9,4,6,8,5,7],
    13:[4,9,5,8,6,7],
    14:[5,9,7,6,8],
    15:[6,9,7,8],
    16:[7,8,9],
    17:[8,9],
    18:[9]
}

gongCheck45=[]
for i in range(9):
    tarr1=[]
    tarr2=[]
    for j in range(9):
        tarr1.append([i,j])
        tarr2.append([j,i])
    gongCheck45.append(tarr1)
    gongCheck45.append(tarr2)

for xk in range(3):
    xindex=xk*3
    for yk in range(3):
        yindex=yk*3
        tarr=[]
        for i in range(3):
            for j in range(3):
                tarr.append([xindex+i,yindex+j])
        gongCheck45.append(tarr)

removeDict={}
for num in sumDict:
    removeDict[num]=[1,2,3,4,5,6,7,8,9]
    for tnum in sumDict[num]:
        removeDict[num].remove(tnum)

removeDictDup={}
for num in sumDictDup:
    removeDictDup[num]=[1,2,3,4,5,6,7,8,9]
    for tnum in sumDictDup[num]:
        removeDictDup[num].remove(tnum)

def initSUDO():
    for i in range(9):
        tarr=[]
        for j in range(9):
            tarr.append([1,2,3,4,5,6,7,8,9])
        sudo.append(tarr)        

    with open(rulesFile,"r") as f:
        for line in f:
            tmp=line.strip().split(",")
            manuRulesSum.append(int(tmp[-1]))
            tarr=[]
            for t in tmp[:-1]:
                tarr.append([int(t[0])-1,int(t[1])-1])
            manuRules.append(tarr)

def updateOne(x,y,num):
    sudo[x][y]=[num]
    for i in range(9):
        if (i!=y and num in sudo[x][i]):
                sudo[x][i].remove(num)

        if (i!=x and num in sudo[i][y]):
                sudo[i][y].remove(num)
    sgx=int(x/3)*3
    sgy=int(y/3)*3
    for i in range(3):
        for j in range(3):
            tx=sgx+i
            ty=sgy+j
            if (tx == x and ty == y):
                continue
            if (num in sudo[tx][ty]):
                sudo[tx][ty].remove(num)


def onlyRemoveNumberNoCheck(x,y,num):
    if (num in sudo[x][y]):
        sudo[x][y].remove(num)
        
def check2NumConflict(arr1,arr2):
    if ((arr1[0] in arr2) or (arr1[1] in arr2) or
        (arr2[0] in arr1) or (arr2[1] in arr1)):
        return 1
    if (getGongPos(arr1[0],arr1[1]) == getGongPos(arr2[0],arr2[1])):
        return 1
    return 0

def getGongPos(x,y):
    return [int(x/3),int(y/3)]

def updateManuRules(targetArr,number):
    for i in range(len(manuRules)):
        if (targetArr in manuRules[i] and len(manuRules[i])!=1):
            manuRules[i].remove(targetArr)
            manuRulesSum[i]=manuRulesSum[i]-number
            manuRules.append([targetArr])
            manuRulesSum.append(number)
    for i in range(len(manuRules)):
        if (len(manuRules[i])==1):
            updateOne(manuRules[i][0][0],manuRules[i][0][1],manuRulesSum[i])

def checkOneNumber():
    for i in range(9):
        for j in range(9):
            if (len(sudo[i][j])==1):
                # print(i,end=",")
                # print(j,end=",")
                # print(sudo[i][j][0])
                updateOne(i,j,sudo[i][j][0])
                updateManuRules([i,j],sudo[i][j][0])
                
def removeTwoSum(rulesTwo,sumnum,InGong):
    if (InGong):
        targetNum=removeDict[sumnum]
        for tr in rulesTwo:
            for num in targetNum:
                onlyRemoveNumberNoCheck(tr[0],tr[1],num)
    else:
        targetNum=removeDictDup[sumnum]
        for tr in rulesTwo:
            for num in targetNum:
                onlyRemoveNumberNoCheck(tr[0],tr[1],num)

def showSUDO():
    tsudo=copy.deepcopy(sudo)
    for i in range(9):
        print(str(i)+":\t",end="")
        for j in range(9):
            tsudo[i][j]=[str(k) for k in tsudo[i][j]]
            if(len(tsudo[i][j])==1):
                print("$"+tsudo[i][j][0]+"$",end="\t")
                continue
            print(",".join(tsudo[i][j]),end="\t")
        print()

def getRemoveList(arr):
    rArr=[1,2,3,4,5,6,7,8,9]
    for a in arr:
        rArr.remove(a)
    return rArr

def removeMutuallyExclusie(x1,y1,x2,y2,removeArr):
    if (x1 == x2):
        for i in range(9):
            if (i == y1 or i==y2):
                continue
            sudo[x1][i]=list(set(sudo[x1][i])-set(removeArr))
            sudo[x1][i].sort()
    
    if (y1 == y2):
         for i in range(9):
            if (i == x1 or i == x2):
                continue
            sudo[i][y1]=list(set(sudo[i][y1])-set(removeArr))
            sudo[i][y1].sort()
            

    if ((int(x1/3) == int(x2/3)) and (int(y1/3)==int(y2/3))):
        xIndex=int(x1/3)*3
        yIndex=int(y1/3)*3
        for i in range(3):
            for j in range(3):
                tx=xIndex+i
                ty=yIndex+j
                if ((tx == x1 and ty == y1)or (tx==x2 and ty==y2)):
                    continue
                sudo[tx][ty]=list(set(sudo[tx][ty])-set(removeArr))
                sudo[tx][ty].sort()

def checkMutuallyExclusive(x,y):
    for i in range(9):
        if (i==x):
            continue
        if (sudo[i][y] == sudo[x][y]):
            removeMutuallyExclusie(i,y,x,y,sudo[i][y])
    for i in range(9):
        if (i==y):
            continue
        if (sudo[x][i] == sudo[x][y]):
            removeMutuallyExclusie(x,i,x,y,sudo[x][i])
    

def checkCellTwoNumber():
    for i in range(9):
        for j in range(9):
            if (len(sudo[i][j])==2):
                checkMutuallyExclusive(i,j)

def SubcheckTwoSum(rulesTwo,sumnum):
    if (len(sudo[rulesTwo[0][0]][rulesTwo[0][1]]) == 2 and sudo[rulesTwo[0][0]][rulesTwo[0][1]]==sudo[rulesTwo[1][0]][rulesTwo[1][1]]):
        return
            
    for num in sudo[rulesTwo[0][0]][rulesTwo[0][1]]:
        if (num >= sumnum or sumnum-num not in sudo[rulesTwo[1][0]][rulesTwo[1][1]]):
            sudo[rulesTwo[0][0]][rulesTwo[0][1]].remove(num)

    for num in sudo[rulesTwo[1][0]][rulesTwo[1][1]]:
        
        if (num >= sumnum or sumnum-num not in sudo[rulesTwo[0][0]][rulesTwo[0][1]]):
            sudo[rulesTwo[1][0]][rulesTwo[1][1]].remove(num)

def checkTwoSum():
    for i in range(len(manuRules)):
        if (len(manuRules[i])==2):
            SubcheckTwoSum(manuRules[i],manuRulesSum[i])
    checkCellTwoNumber()

def checkGong45():
    for gong in gongCheck45:
        tlist=[]
        tlistInternal=[]
        tsum=0
        tsumInternal=0
        for i in range(len(manuRules)):
            label=0
            allInGong=1
            for ttrule in manuRules[i]:
                if (ttrule in gong):
                    label=1
                if (ttrule not in gong):
                    allInGong=0

            if (allInGong):
                tlistInternal=tlistInternal+manuRules[i]
                tsumInternal+=manuRulesSum[i]

            if (label):
                tlist=tlist+manuRules[i]
                tsum+=manuRulesSum[i]

        if (len(tlistInternal)==8):
            for g in gong:
                if (g not in tlistInternal):
                    updateOne(g[0],g[1],45-tsumInternal)

        if (len(tlistInternal)==7):
            tarr=[]
            for g in gong:
                if (g not in tlistInternal):
                    tarr.append(g)
            updateManuRules(tarr,tsum-45)
            removeTwoSum(tarr,45-tsumInternal,1)
            checkCellTwoNumber()
            checkOneNumber()

        if (len(tlist)==10):
            for t in tlist:
                if(t not in gong):
                    updateOne(t[0],t[1],tsum-45)
                    checkOneNumber()
                    break
                
        if (len(tlist)==11):
                tarr=[]
                for t in tlist:
                    if(t not in gong):
                        tarr.append(t)
                removeTwoSum(tarr,tsum-45,check2NumConflict(tarr[0],tarr[1]))
                SubcheckTwoSum(tarr,tsum-45)
                checkCellTwoNumber()
                checkOneNumber()

initSUDO()
for i in range(len(manuRules)):
    if (len(manuRules[i])==1):
        updateOne(manuRules[i][0][0],manuRules[i][0][1],manuRulesSum[i])

for i in range(len(manuRules)):
    if (len(manuRules[i])==2):
        removeTwoSum(manuRules[i],manuRulesSum[i],1)

for i in range(10):
    checkGong45()
    checkOneNumber()
    checkTwoSum()

showSUDO()

print("If it does not solve this sudoku, raise the number of loops in line 283 of the code.")