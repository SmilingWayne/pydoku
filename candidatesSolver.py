from datetime import datetime
import numpy as np
from collections import Counter
from Utils import *

# 试着用位运算进行优化！

def WriteOnlyBackNum(sodokuArr, backupArr):
    # 根据已填值计算备选结果
    # 行备选
    for rowIndex in range(9):
        rowArr = [str(x) for x in sodokuArr[rowIndex] if x > 0]
        for colIndex in range(9): backupArr[rowIndex, colIndex] = ''.join([x for x in backupArr[rowIndex, colIndex] if not x in rowArr])
    # 列备选
    for colIndex in range(9):
        colArr = [str(x) for x in sodokuArr[:,colIndex] if x > 0]
        for rowIndex in range(9): backupArr[rowIndex, colIndex] = ''.join([x for x in backupArr[rowIndex, colIndex] if not x in colArr])
    # 区域备选
    for regionIndex in range(9):
        regionArr = [str(x) for x in sodokuArr[regionIndex // 3 * 3 : regionIndex // 3 * 3 + 3, regionIndex % 3 * 3 : regionIndex % 3 * 3 + 3].reshape(-1) if x > 0]
        regionBackupArr = backupArr[regionIndex // 3 * 3 : regionIndex // 3 * 3 + 3, regionIndex % 3 * 3 : regionIndex % 3 * 3 + 3]
        for rowIndex in range(3):
            for colIndex in range(3):
                regionBackupArr[rowIndex, colIndex] = ''.join([x for x in regionBackupArr[rowIndex, colIndex] if not x in regionArr])
    
    # 根据备选结果计算唯一备选
    # 行备选
    for rowIndex in range(9):
        rowArr = []
        for item in backupArr[rowIndex]: 
            rowArr += list(item)
        onlyBackupArr = [x[0] for x in Counter(rowArr).most_common() if x[1] == 1]
        for colIndex in range(9):
            if len([x for x in backupArr[rowIndex, colIndex] if x in onlyBackupArr]) > 0:
                backupArr[rowIndex, colIndex] = [x for x in onlyBackupArr if x in backupArr[rowIndex, colIndex]][0]
    # 列备选
    for colIndex in range(9):
        colArr = []
        for item in backupArr[:,colIndex]: colArr += list(item)
        onlyBackupArr = [x[0] for x in Counter(colArr).most_common() if x[1] == 1]
        for rowIndex in range(9):
            if len([x for x in backupArr[rowIndex, colIndex] if x in onlyBackupArr]) > 0:
                backupArr[rowIndex, colIndex] = [x for x in onlyBackupArr if x in backupArr[rowIndex, colIndex]][0]
    # 区域备选
    for regionIndex in range(9):
        regionArr = []
        regionBackupArr = backupArr[regionIndex // 3 * 3 : regionIndex // 3 * 3 + 3, regionIndex % 3 * 3 : regionIndex % 3 * 3 + 3]
        for item in regionBackupArr.reshape(-1): regionArr += list(item)
        onlyBackupArr = [x[0] for x in Counter(regionArr).most_common() if x[1] == 1]
        for rowIndex in range(3):
            for colIndex in range(3):
                if len([x for x in regionBackupArr[rowIndex, colIndex] if x in onlyBackupArr]) > 0:
                    regionBackupArr[rowIndex, colIndex] = [x for x in onlyBackupArr if x in regionBackupArr[rowIndex, colIndex]][0]

    # 计算是否存在唯一备选
    __backupArr = np.array(np.where(backupArr == '', '0', backupArr), np.int)
    status = len([x for x in __backupArr.reshape(-1) if x >= 1 and x <= 9]) > 0

    # 填充唯一备选
    backupArr = np.where((__backupArr >= 1) & (__backupArr <= 9), '', __backupArr)
    backupArr = np.where(backupArr == '0', '', backupArr)
    sodokuArr = np.where((__backupArr >= 1) & (__backupArr <= 9), __backupArr, sodokuArr)

    return status, sodokuArr, backupArr

def CheckNum(sodokuArr, zeroTest: bool = False):
    # 零值检测
    if zeroTest:
        for rowIndex in range(9):
            rowArr = [x for x in sodokuArr[rowIndex] if x == 0]
            if len(rowArr) > 0: return False

    # 行检验
    for rowIndex in range(9):
        rowArr = [x for x in sodokuArr[rowIndex] if x > 0]
        if len(rowArr) > 0:
            counter = Counter(rowArr).most_common()[0]
            if counter[1] > 1: return False
    # 列检验
    for colIndex in range(9):
        colArr = [x for x in sodokuArr[:,colIndex] if x > 0]
        if len(colArr) > 0:
            counter = Counter(colArr).most_common()[0]
            if counter[1] > 1: return False
    # 区域检验
    for regionIndex in range(9):
        regionArr = [x for x in sodokuArr[regionIndex // 3 * 3 : regionIndex // 3 * 3 + 3, regionIndex % 3 * 3 : regionIndex % 3 * 3 + 3].reshape(-1) if x > 0]
        if len(regionArr) > 0:
            counter = Counter(regionArr).most_common()[0]
            if counter[1] > 1: return False

    return True

def GetTestBackNum(backupArr):
    backupList = []
    # 选择行/列/区域中被备选数最多的备选
    # 行备选
    for rowIndex in range(9):
        rowArr = [x for x in backupArr[rowIndex] if x != '']
        if len(rowArr) > 0:
            rowArr = sorted(Counter(rowArr).most_common(), key = lambda x: (-len(x[0])))
            backupList.append(rowArr[0])
    # 列备选
    for colIndex in range(9):
        colArr = [x for x in backupArr[:,colIndex] if x != '']
        if len(colArr) > 0:
            colArr = sorted(Counter(colArr).most_common(), key = lambda x: (-len(x[0])))
            backupList.append(colArr[0])
    # 区域备选
    for regionIndex in range(9):
        regionBackupArr = backupArr[regionIndex // 3 * 3 : regionIndex // 3 * 3 + 3, regionIndex % 3 * 3 : regionIndex % 3 * 3 + 3]
        regionArr = [x for x in regionBackupArr.reshape(-1) if x != '']
        if len(regionArr) > 0:
            regionArr = sorted(Counter(regionArr).most_common(), key = lambda x: (-len(x[0])))
            backupList.append(regionArr[0])
    # 计算备选出现次数, 返回出现长度最短且频率最高的, 出现频率最高, 意味着其影响的范围最广
    dictBackupCounter = {}
    for item in backupList:
        backupNum, count = item
        if backupNum in dictBackupCounter: dictBackupCounter[backupNum] += count
        else: dictBackupCounter[backupNum] = count
    backupList = sorted(dictBackupCounter.items(), key = lambda x: (len(x[0]), -x[1]))
    backupList = [x[0] for x in backupList]

    # 查找备选测试位置
    if len(backupList) > 0:
        for rowIndex in range(9):
            for colIndex, backupNum in enumerate(backupArr[rowIndex]):
                if backupNum == backupList[0]:
                    return (rowIndex, colIndex), list(backupNum)

    return (-1, -1), ['']

@runtime_display
def main():

        sodoku: list = [
            # 世界上最难的数独
            [ 8, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 3, 6, 0, 0, 0, 0, 0 ],
            [ 0, 7, 0, 0, 9, 0, 2, 0, 0 ],
            [ 0, 5, 0, 0, 0, 7, 0, 0, 0 ],
            [ 0, 0, 0, 0, 4, 5, 7, 0, 0 ],
            [ 0, 0, 0, 1, 0, 0, 0, 3, 0 ],
            [ 0, 0, 1, 0, 0, 0, 0, 6, 8 ],
            [ 0, 0, 8, 5, 0, 0, 0, 1, 0 ],
            [ 0, 9, 0, 0, 0, 0, 4, 0, 0 ],
        ]
        sodokuArr: np.array = np.array(sodoku, np.int)

        # 初始化备选数组
        backupArr: np.array = np.array([['123456789' for x in range(9)] for x in range(9)])
        backupArr = np.where(sodokuArr == 0, backupArr, '')

        testPositionRecordList: list = []
        dictTestPositionRecord: dict = {}
        while True:
            status, __sodokuArr, __backupArr = WriteOnlyBackNum(sodokuArr, backupArr)
            sodokuArr = __sodokuArr.copy()
            backupArr = __backupArr.copy()

            position: tuple = (-1, -1)
            backupNumList: list = []

            if not status:
                # 获取测试备选
                position, backupNumList = GetTestBackNum(backupArr)
                sodokuArrRd: np.array = sodokuArr.copy()
                backupArrRd: np.array = backupArr.copy()
                
                if not CheckNum(sodokuArr):
                    # 如果一开始题目里就存在重复项, 则说明题目有问题
                    if len(testPositionRecordList) == 0:
                        # endTime = datetime.now()
                        # message = '题目异常'
                        break
                    
                    # 否则, 则说明在填入的测试数字不能得到最终解, 需要重置回填写之前
                    sodokuArr = dictTestPositionRecord[testPositionRecordList[-1]]['sodoku'].copy()
                    backupArr = dictTestPositionRecord[testPositionRecordList[-1]]['backup'].copy()
                else:
                    # 当题目校验为正确且没有需要填入测试数字的坐标时, 则说明解题完成
                    if position == (-1, -1):
                        if not CheckNum(sodokuArr, True):
                            position = testPositionRecordList[-1]
                            backupNumList =  dictTestPositionRecord[position]['backupNumList']
                            sodokuArr = dictTestPositionRecord[position]['sodoku'].copy()
                            backupArr = dictTestPositionRecord[position]['backup'].copy()
                            continue
                        else:
                            # endTime = datetime.now()
                            status = True
                            # message = '解题完成'
                            break
                    
                    # 否则, 则需要填入测试数字, 测试数字从每一个坐标的全部备选数字中获取
                    # 不断尝试填入备选数字, 直至无解时, 返回上一个坐标的测试数字, 如此循环, 直至最终无解
                    if position in dictTestPositionRecord:
                        # 排除已填过的备选数字
                        testNumList = dictTestPositionRecord[position]['testNumList']
                        backupNumList = [x for x in backupNumList if not x in testNumList]
                        if len(backupNumList) > 0:
                            x, y = position
                            testNum: int = int(backupNumList[0])
                            sodokuArr[x, y] = testNum
                            backupArr[x, y] = ''

                            # 记录已填入的备选数字
                            # testIndex += 1
                            backupNumList.remove(str(testNum))
                            if len(backupNumList) > 0:
                                dictTestPositionRecord[position]['testNumList'].append(str(testNum))
                                dictTestPositionRecord[position]['backupNumList'] = backupNumList
                            else:
                                testPositionRecordList.remove(position)
                                dictTestPositionRecord.pop(position)
                        else:
                            # 如果当前坐标的全部备选均已用完, 则在记录中删除该坐标
                            testPositionRecordList.remove(position)
                            dictTestPositionRecord.pop(position)

                            # 如果删除当前坐标后仍然存在其他坐标, 则重置回上一个坐标
                            if len(testPositionRecordList) > 0:
                                sodokuArr = dictTestPositionRecord[testPositionRecordList[-1]]['sodoku'].copy()
                                backupArr = dictTestPositionRecord[testPositionRecordList[-1]]['backup'].copy()
                            else:
                                # 全部备选均已用完, 说明该数独可能无解
                                # endTime = datetime.now()
                                # message = '全部备选均已用完, 该数独可能无解'
                                break
                    else:
                        if not position in testPositionRecordList: testPositionRecordList.append(position)
                        # testDeep = (lambda x, y : x if x > y else y)(len(testPositionRecordList), testDeep)
                        dictTestPositionRecord[position] = { 'testNumList': [], 'backupNumList': [], 'sodoku': sodokuArrRd, 'backup': backupArrRd }
                # 

if __name__ == '__main__':
    # 解题开始


    startTime: datetime = datetime.now()  # 开始时间
    endTime: datetime = startTime         # 结束时间
    testIndex: int = 0                    # 测试次数
    runIndex: int = 0                     # 计算周期
    testDeep: int = 0                     # 测试深度
    status: bool = False                  # 解题状态
    message: str = ''                     # 返回说明
    
    # 初始化题目
  # runIndex += 1
    main()
    # print('开始时间: ', startTime)
    # print('结束时间: ', endTime)         
    # print('解题时间: ', endTime - startTime)
    # print('测试次数: ', testIndex)                    
    # print('计算周期: ', runIndex)                    
    # print('最大深度: ', testDeep)                     
    # print('解题状态: ', '成功' if status else '失败')                  
    # print('解题结果: ', message)                     
    # print(sodokuArr)

