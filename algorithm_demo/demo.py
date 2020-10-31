from collections import defaultdict
import random
import time
from typing import DefaultDict, Dict, List, Callable, Tuple
import numpy as np

class Component():
    '''测试用的Component对象

    属性：
        strokeList: 模拟笔画序列。字符串表示，一位为一笔。
        topoStr: 模拟拓扑序列。字符串表示，拓扑关系矩阵下三角的合并。
        length: 笔画序列长度。
        topoSliceCache: 拓扑切片的缓存。
        topoRowCache: 拓扑行切片的缓存
    '''
    def __init__(self, strokeList: str, topoStr: str):
        self.strokeList     = strokeList
        self.topoStr        = topoStr
        self.length         = len(strokeList)
        self.topoSliceCache = { 1 : '' }
        self.topoRowCache   = { 0 : '' }

    def getTopoSlice(self, indexList: List[int]):
        binaryCode = self.indexListToBinaryCode(indexList)
        if binaryCode in self.topoSliceCache:
            return self.topoSliceCache[binaryCode]
        topoSlice = ''
        length = len(indexList)
        for n in range(1, length):
            index = indexList[n]
            offset = int(index * (index - 1) / 2)
            for beforeN in range(0, n):
                topoSlice += self.topoStr[offset + indexList[beforeN]]
        self.topoSliceCache[binaryCode] = topoSlice
        return topoSlice

    def getTopoRow(self, row: int):
        if row in self.topoRowCache:
            return self.topoRowCache[row]
        k = int(row * (row - 1) / 2)
        topoStr = self.topoStr[k:k+row]
        self.topoRowCache[row] = topoStr
        return topoStr

    def indexListToBinaryCode(self, indexList: List[int]):
        length = self.length
        binary = 0
        for index in indexList:
            binary += 1 << (length - index - 1)
        return binary

    def clearCache(self):
        self.topoRowCache = { 0 : '' }
        self.topoSliceCache = { 1 : '' }

    def __str__(self):
        return f'list:{self.strokeList} topo:{self.topoStr}'

    def __eq__(self, other):
        if not isinstance(other,Component):
            return NotImplemented
        return self.strokeList == other.strokeList and self.topoStr == other.topoStr

def findSliceV1(component: Component, root: Component):
    '''check topo on each step'''
    cLength = component.length
    rLength = root.length
    result: List[int] = []
    if cLength < rLength:
        return result
    cStrokeList = component.strokeList
    rStrokeList = root.strokeList
    rFirstStroke = rStrokeList[0]
    lengthLimit = cLength - rLength + 1
    validIndexLists: List[List[int]] = []
    for cIndex in range(0, lengthLimit):
        if cStrokeList[cIndex] == rFirstStroke:
            validIndexLists.append([cIndex])
    if len(validIndexLists) == 0:
        return result
    for rIndex in range(1,rLength):
        newValidIndexLists: List[List[int]] = []
        end = lengthLimit + rIndex
        for indexList in validIndexLists:
            for cIndex in range(indexList[-1]+1,end):
                if cStrokeList[cIndex] == rStrokeList[rIndex]:
                    tmpCTopoStr = component.getTopoRow(cIndex)
                    cTopoStrRow = ''
                    for i in indexList:
                        cTopoStrRow += tmpCTopoStr[i]
                    rTopoStrRow = root.getTopoRow(rIndex)
                    if cTopoStrRow == rTopoStrRow:
                        newValidIndexLists.append(indexList + [cIndex])
        if len(newValidIndexLists) == 0:
            return result
        else:
            validIndexLists = newValidIndexLists
    for indexList in validIndexLists:
        result.append(component.indexListToBinaryCode(indexList))
    return result

def findSliceV1_1(component: Component, root: Component):
    '''分段查找'''
    cLength = component.length
    rLength = root.length
    result: List[int] = []
    if cLength < rLength:
        return result
    cStrokeList = component.strokeList
    rStrokeList = root.strokeList
    rFirstStroke = rStrokeList[0]
    end = cLength - rLength + 1
    validIndexLists: List[List[int]] = []
    for cIndex in range(0, end):
        if cStrokeList[cIndex] == rFirstStroke:
            validIndexLists.append([cIndex])
    if len(validIndexLists) == 0:
        return result
    for rIndex in range(1, rLength):
        newValidIndexLists: List[List[int]] = []
        end = end + 1
        range_ = [x[-1] + 1 for x in validIndexLists] + [end]
        for i in range(0, len(range_) - 1):
            for cIndex in range(range_[i],range_[i+1]):
                if cStrokeList[cIndex] == rStrokeList[rIndex]:
                    tmpCTopoStr = component.getTopoRow(cIndex)
                    rTopoStrRow = root.getTopoRow(rIndex)
                    for j in range(0, i + 1):
                        indexList = validIndexLists[j]
                        cTopoStrRow = ''
                        for idx in indexList:
                            cTopoStrRow += tmpCTopoStr[idx]
                        if cTopoStrRow == rTopoStrRow:
                            newValidIndexLists.append(indexList + [cIndex])
        if len(newValidIndexLists) == 0:
            return result
        else:
            validIndexLists = newValidIndexLists
    for indexList in validIndexLists:
        result.append(component.indexListToBinaryCode(indexList))
    return result

def findSliceV2(component: Component, root: Component):
    '''check topo on final stage'''
    cLength = component.length
    rLength = root.length
    result: List[int] = []
    if cLength < rLength:
        return result
    cStrokeList = component.strokeList
    rStrokeList = root.strokeList
    lengthLimit = cLength - rLength + 1
    rFirstStroke = rStrokeList[0]
    validIndexLists: List[List[int]] = []
    for cIndex in range(0,lengthLimit):
        if cStrokeList[cIndex]==rFirstStroke:
            validIndexLists.append([cIndex])
    if len(validIndexLists)==0:
        return result
    else:
        for rIndex in range(1, rLength):
            newValidIndexLists: List[List[int]] = []
            end = lengthLimit + rIndex
            for indexList in validIndexLists:
                for cIndex in range(indexList[-1] + 1,end):
                    if cStrokeList[cIndex] == rStrokeList[rIndex]:
                        newIndexList = indexList + [cIndex]
                        newValidIndexLists.append(newIndexList)
            if len(newValidIndexLists) == 0:
                return result
            else:
                validIndexLists = newValidIndexLists
    for indexList in validIndexLists:
        if component.getTopoSlice(indexList) == root.topoStr:
            result.append(component.indexListToBinaryCode(indexList))
    return result

def findSliceV2_1(component: Component, root: Component):
    '''分段查找'''
    cLength = component.length
    rLength = root.length
    result: List[int] = []
    if cLength < rLength:
        return result
    cStrokeList = component.strokeList
    rStrokeList = root.strokeList
    end = cLength - rLength + 1
    rFirstStroke = rStrokeList[0]
    validIndexLists: List[List[int]] = []
    for cIndex in range(0,end):
        if cStrokeList[cIndex]==rFirstStroke:
            validIndexLists.append([cIndex])
    if len(validIndexLists)==0:
        return result
    for rIndex in range(1, rLength):
        newValidIndexLists: List[List[int]] = []
        end = end + 1
        range_ = [x[-1] + 1 for x in validIndexLists] + [end]
        for i in range(0, len(range_) - 1):
            for cIndex in range(range_[i],range_[i+1]):
                if cStrokeList[cIndex] == rStrokeList[rIndex]:
                    for j in range(0, i + 1):
                        newIndexList = validIndexLists[j] + [cIndex]
                        newValidIndexLists.append(newIndexList)
        if len(newValidIndexLists) == 0:
            return result
        else:
            validIndexLists = newValidIndexLists
    for indexList in validIndexLists:
        if component.getTopoSlice(indexList) == root.topoStr:
            result.append(component.indexListToBinaryCode(indexList))
    return result

def findSliceV3(component: Component, root: Component):
    '''generator version'''
    cStrokeList = component.strokeList
    rStrokeList = root.strokeList
    def gener(start, end, rStrokeIndex, indexList):
        start_ = start
        while start_ <= end:
            iIndexList = indexList.copy()
            try:
                index = cStrokeList[start_:end+1].index(rStrokeList[rStrokeIndex]) + start_
                start_ = index + 1
                iIndexList.append(index)
                if rStrokeIndex < len(rStrokeList) - 1:
                    for iiIndexList in gener(start_, end+1, rStrokeIndex+1, iIndexList.copy()):
                        yield iiIndexList
                else:
                    yield iIndexList
            except:
                break
    result = []
    for indexList in gener(0, len(cStrokeList) - len(rStrokeList), 0, []):
        if component.getTopoSlice(indexList) == root.topoStr:
            result.append(component.indexListToBinaryCode(indexList))
    return result

def findAllValidCombinations(
    component: Component,
    roots: List[Component],
    findSliceFn: Callable[[Component,Component],List[int]]):
    binaryDict: Dict[int,Component] = {}
    for root in roots:
        sliceBinaryList = findSliceFn(component, root)
        for sliceBinary in sliceBinaryList:
            binaryDict[sliceBinary] = root
    sliceBinaryList = list(binaryDict.keys())
    listLength = len(sliceBinaryList)
    tmpResult : List[Tuple[int,...]] = []
    if listLength == 0:
        return tmpResult
    sliceBinaryList.sort(reverse=True)
    finishBinary = 2 ** len(component.strokeList) - 1
    firstStrokeBinary = 2 ** (len(component.strokeList) - 1)
    def combineNext(
        currentBinary: int,
        currentCombination: Tuple[int,...],
        startFromIndex: int):
        for index in range(startFromIndex, listLength):
            binary = sliceBinaryList[index]
            if currentBinary & binary == 0:
                newBinary = currentBinary + binary
                expandedCombination = currentCombination + (binary,)
                if newBinary == finishBinary:
                    tmpResult.append(expandedCombination)
                else:
                    combineNext(newBinary, expandedCombination, index + 1)
    for index in range(0, listLength):
        b = sliceBinaryList[index]
        if not b & firstStrokeBinary:
            break
        combineNext(b, (b,), index+1)
    result = []
    for t in tmpResult:
        result.append((binaryDict[i] for i in t))
    return result

def findAllValidCombinationsV2(
    component: Component,
    roots: List[Component],
    findSliceFn: Callable[[Component,Component],List[int]]):
    '''binary search version'''
    binaryDict: Dict[int,Component] = {}
    for root in roots:
        sliceBinaryList = findSliceFn(component, root)
        for sliceBinary in sliceBinaryList:
            binaryDict[sliceBinary] = root
    sliceBinaryList = list(binaryDict.keys())
    listLength = len(sliceBinaryList)
    tmpResult : List[Tuple[int,...]] = []
    if listLength == 0:
        return tmpResult
    sliceBinaryList.sort(reverse=True)
    cLength = len(component.strokeList)
    finishBinary = 2 ** cLength - 1
    def binarySearch(target: int):
        front = 0
        rear = listLength - 1
        while front < rear:
            mid = (front + rear) // 2
            if sliceBinaryList[mid] > target:
                front = mid + 1
            else:
                rear = mid
        return front
    def combineNext(
        currentBinary: int,
        currentCombination: Tuple[int,...]):
        missingBinary = finishBinary - currentBinary
        firstMissingBinary = 2 ** (len(bin(missingBinary)) - 3)
        start = binarySearch(missingBinary)
        end= binarySearch(firstMissingBinary)
        for index in range(start, end+1):
            binary = sliceBinaryList[index]
            if currentBinary & binary == 0:
                newBinary = currentBinary + binary
                expandedCombination = currentCombination + (binary,)
                if newBinary == finishBinary:
                    tmpResult.append(expandedCombination)
                else:
                    combineNext(newBinary, expandedCombination)
    combineNext(0,())
    result: List[Tuple[Component,...]] = []
    for t in tmpResult:
        result.append((binaryDict[i] for i in t))
    return result

def findAllValidCombinationsV3(
    component: Component,
    roots: List[Component],
    findSliceFn: Callable[[Component,Component],List[int]]):
    sbd: DefaultDict[int, List[Tuple[int,Component]]] = defaultdict(list)
    for root in roots:
        for sliceBinary in findSliceFn(component, root):
            sbd[len(bin(sliceBinary))].append((sliceBinary,root))
    finishBinary = 2 ** len(component.strokeList) - 1
    result: List[Tuple[Component,...]] = []
    def combineNext(
        currentBinary: int,
        currentCombination: Tuple[int,...],
        tryFrom: List[Tuple[int,Component]]):
        for i in tryFrom:
            if currentBinary & i[0] != 0:
                continue
            nextCombination = currentCombination + (i[1],)
            nextBinary = currentBinary + i[0]
            if nextBinary == finishBinary:
                result.append(nextCombination)
            else:
                residue = finishBinary - nextBinary
                combineNext(nextBinary, nextCombination, sbd[len(bin(residue))])
    if sbd:
        combineNext(0,(),sbd[len(bin(finishBinary))])
    return result

def findAllValidCombinationsV4(
    component: Component,
    roots: List[Component],
    findSliceFn: Callable[[Component,Component],List[int]]):
    binaryDict: Dict[int,Component] = {}
    for root in roots:
        sliceBinaryList = findSliceFn(component, root)
        for sliceBinary in sliceBinaryList:
            binaryDict[sliceBinary] = root
    sliceBinaryList = list(binaryDict.keys())
    listLength = len(sliceBinaryList)
    tmpResult : List[Tuple[int,...]] = []
    if listLength == 0:
        return tmpResult
    sliceBinaryList.sort()
    finishBinary = 2 ** component.length - 1
    def combineNext(
        currentBinary: int,
        currentCombination: Tuple[int,...]):
        missingBinary = finishBinary - currentBinary
        firstMissingBinary = 2 ** (len(bin(missingBinary)) - 3)
        start = np.searchsorted(sliceBinaryList, missingBinary, side='left')
        end= np.searchsorted(sliceBinaryList, firstMissingBinary)
        start = start if not start == listLength else start - 1
        for index in range(start, end-1, -1):
            binary = sliceBinaryList[index]
            if currentBinary & binary == 0:
                newBinary = currentBinary + binary
                expandedCombination = currentCombination + (binary,)
                if newBinary == finishBinary:
                    tmpResult.append(expandedCombination)
                else:
                    combineNext(newBinary, expandedCombination)
    combineNext(0,())
    result: List[Tuple[Component,...]] = []
    for t in tmpResult:
        result.append((binaryDict[i] for i in t))
    return result

#### test utils
def randomStrokeList(n: int) -> str:
    '''随机生成n笔画字的笔画序列。笔画用数字字符串表示。

    参数：
        n：笔画序列长度

    输出：
        首位不为'0'的阿拉伯数字字符串，长度为 n 。
    '''
    return str(random.randint(10**(n-1),10**(n)-1))

def randomTopoStr(n: int) -> str:
    '''随机生成 n 笔字的 topo 序列。等效于把 pychai 当中的 topologyMatrix 合成一串字符串。

    参数：
        n：笔画序列的长度

    输出：
        仅由'0','1','2','3','4'组成的字符串，长度为 (n*(n-1))/2
    '''
    return ''.join([ str(random.randint(0,4)) for _ in range(int((n*(n-1))/2))])

def randomComponents(strokeLength: int, howMany: int):
    '''批量生成随机的、属性不重复的 Component

    参数：
        strokeLength：生成 Component 的笔画长度。
        howMany：生成的个数

    输出：
        包含所有随机生成 Component 的列表
    '''
    components = [Component(randomStrokeList(strokeLength),randomTopoStr(strokeLength))]
    count = 0
    while count < howMany:
        newComponent = Component(randomStrokeList(strokeLength),randomTopoStr(strokeLength))
        for component in components:
            if component == newComponent:
                break
            else:
                components.append(newComponent)
                count+=1
    return components

def testSliceFn(
    components: List[Component],
    roots: List[Component],
    testFn: Callable[[Component,Component],List[int]]):
    '''测试「取切片函数」运行效率的函数

    无输出。在控制台打印相关数据。

    参数：
        components：待拆分的字集合
        roots：字根集合
        testFn：被测试的「取切片函数」
    '''
    totalTimes = len(components) * len(roots)
    successTimes = 0
    failureElapsed = 0
    successElapsed = 0
    start = time.time()
    for component in components:
        for root in roots:
            t = time.time()
            result = list(testFn(component,root))
            elapsed = time.time() - t
            if len(result)>0:
                successTimes += 1
                successElapsed += elapsed
            else:
                failureElapsed += elapsed
    totalElapsed = time.time() - start
    failureTimes = totalTimes - successTimes
    successAvg = successElapsed/successTimes*1000000 if successTimes!=0 else 0
    failureAvg = failureElapsed/failureTimes*1000000 if failureTimes!=0 else 0
    print(f'success:{successTimes:d} successAvg:{successAvg:.2f} failure:{(totalTimes-successTimes):d} failureAvg:{failureAvg:.2f} totalTimeElapsed:{int(totalElapsed*1000):d}ms')

def testCombinationFn(
    components: List[Component],
    roots: List[Component],
    testFn: Callable[[Component,List[Component]],list]):
    '''测试「查找可行根组合函数」运行效率的函数

    输出耗时(ms)。并在控制台打印数据。

    参数：
        components：待拆字集合
        roots：字根集合
        testFn：被测试的「查找可行根组合函数」

    输出：
        测试总用时(ms)
    '''
    successElapsed = 0
    failureElapsed = 0
    start = time.time()
    for component in components:
        t1 = time.time()
        r = testFn(component,roots)
        elapsed = time.time() - t1
        if len(r)>0:
            successElapsed += elapsed
        else:
            failureElapsed += elapsed
    totalElapsed = time.time() - start
    print(f'totalTimeElapsed:{int(totalElapsed*1000)}ms')
    return int(totalElapsed*1000)

def clearAllCache(components: List[Component]):
    '''清除所有 component 的 topo 切片缓存'''
    for component in components:
        component.clearCache()

def checkCorrectness(*fns: Callable[[Component,Component],List[List[Component]]]):
    # 生成一个“天”字
    component = Component('横横撇点','散连交散连连')
    roots = [
        Component('横',''),            #根“一”
        Component('横横','散'),        #根“二”
        Component('撇点','连'),        #根“人”
        Component('横撇点','交连连'),  #根“大”
        Component('撇',''),            #根“丿”
        Component('点','')             #根“丶”
    ]
    for fn in fns:
        print('-----------')
        result = fn(component,roots)
        for schemeList in result:
            for r in schemeList:
                print(r.strokeList)
            print()
        print('Finished')

def combinationToStr(components: List[Component]):
    return ' '.join([ str(c) for c in components])

def combinationsToStr(combinations: List[List[Component]]):
    tmp = list(map(combinationToStr, combinations))
    tmp.sort()
    return tmp

# def performanceComparisonGraph(*fns: Callable[[Component,List[Component]],List[List[Component]]]):
#     # components = sum([
#     #     randomComponents(2,49),
#     #     randomComponents(3,76),
#     #     randomComponents(4,106),
#     #     randomComponents(5,79),
#     #     randomComponents(6,55),
#     #     randomComponents(7,43),
#     #     randomComponents(8,35),
#     #     randomComponents(9,18),
#     #     randomComponents(10,10),
#     #     randomComponents(11,6),
#     #     ],[])
#     singleStrokeRoots = [
#         Component('1',''), Component('2',''), Component('3',''), Component('4',''),
#         Component('5',''), Component('6',''), Component('7',''), Component('8',''),
#         Component('9',''), Component('0','')]
#     x = []
#     ys = []
#     for i in range(0,len(fns)):
#         ys.append([])
#     for componentStrokeNum in range(30,32):
#         print(componentStrokeNum)
#         x.append(componentStrokeNum)
#         components = randomComponents(componentStrokeNum,1000)
#         roots = sum([singleStrokeRoots,
#             randomComponents(2,50),
#             randomComponents(3,50),
#             randomComponents(4,50),
#             randomComponents(5,50)
#             ],[])
#         for i in range(0,len(fns)):
#             y = testCombinationFn(components,roots,fns[i])
#             ys[i].append(y)
#             clearAllCache(components)
#             clearAllCache(roots)
#     import matplotlib.pyplot as plt
#     colors = ['green', 'blue', 'yellow', 'pink', 'red']
#     plt.title('comparison')
#     for i in range(0,len(ys)):
#         plt.plot(x,ys[i],color=colors[i],label=str(i))
#     plt.legend()
#     plt.xlabel('stroke num')
#     plt.ylabel('time elapsed(ms)')
#     plt.show()

#### run tests

def wrapV1(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV1)

def wrapV2(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV2)

def wrapV1_1(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV1_1)

def wrapV2_1(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV2_1)

def wrapV3(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV3)

def w1(component: Component,roots: List[Component]):
    return findAllValidCombinations(component,roots,findSliceV1)

def w2(component: Component,roots: List[Component]):
    return findAllValidCombinationsV2(component,roots,findSliceV1)

def w3(component: Component,roots: List[Component]):
    return findAllValidCombinationsV3(component,roots,findSliceV1)

def w4(component: Component,roots: List[Component]):
    return findAllValidCombinationsV4(component,roots,findSliceV1)

# test1

# components = sum([
#     randomComponents(8,100),
#     randomComponents(9,100),
#     randomComponents(14,100),
#     randomComponents(15,100),
#     randomComponents(16,100),
#     randomComponents(17,100),
#     randomComponents(23,100),
#     randomComponents(24,100),
#     randomComponents(26,100),
#     randomComponents(28,100),
#     randomComponents(28,100),
#     randomComponents(30,100),
# ],[])
# components = randomComponents(30, 1000)
# singleStrokeRoots = [Component('1',''), Component('2',''), Component('3',''),
#     Component('4',''), Component('5',''), Component('6',''), Component('7',''),
#     Component('8',''), Component('9',''), Component('0','')]
# roots = sum([singleStrokeRoots,
#     randomComponents(2,50),
#     randomComponents(3,50),
#     randomComponents(4,60),
#     randomComponents(5,60),
# ],[])
# testSliceFn(components,roots,findSliceV1)
# clearAllCache(components)
# clearAllCache(roots)
# testSliceFn(components,roots,findSliceV2)
# clearAllCache(components)
# clearAllCache(roots)
# testSliceFn(components,roots,findSliceV1_1)
# clearAllCache(components)
# clearAllCache(roots)
# testSliceFn(components,roots,findSliceV2_1)
# clearAllCache(components)
# clearAllCache(roots)
# testSliceFn(components,roots,findSliceV3)

# test2
# checkCorrectness(w4)

# test3
# performanceComparisonGraph(w2,w3)

# test4
components = randomComponents(8,500)
singleStrokeRoots = [Component('1',''), Component('2',''), Component('3',''),
    Component('4',''), Component('5',''), Component('6',''), Component('7',''),
    Component('8',''), Component('9',''), Component('0','')]
roots = sum([singleStrokeRoots,
    randomComponents(2,50),
    randomComponents(3,50),
    randomComponents(4,60),
    randomComponents(5,60),
],[])
testCombinationFn(components,roots,w2)
clearAllCache(components)
clearAllCache(roots)
testCombinationFn(components,roots,w4)
