'''
经典形码
'''

from typing import Dict, List, Tuple
from .chai import Chai
from ..base import Component, Compound

class Sequential(Chai):
    '''
    经典形码
    '''
    @staticmethod
    def genSliceBinaries(component: Component, root: Component):
        '''找出一个根在一个部件字中的所有有效切片

        V1版本，会在每匹配到一个笔画时就检查拓扑。

        参数:
            component: 待拆部件
            root: 根部件

        输出:
            List[int]: 根部件在待拆部件中的所有有效切片，切片用二进制表示。没有找到切片时返回
            空列表。
            例: 待拆部件“天”，根部件“大”。“大”在“天”中的有效的切片为“天”的第2、3、4笔。“天”
            的笔画列表为['横', '横', '撇', '捺']，每一位都取用 index 列表表示为[0,1,2,3]
            二进制表示为 0b1111 ，只取后三笔用 index 列表表示为[1,2,3]，二进制表示为 0b0111，
            即整型数字 7 。故输出为 [7]。
        '''
        cpnStrokeList = component.strokeList
        rStrokeList = root.strokeList
        cpnLength = len(cpnStrokeList)
        rootLength = len(rStrokeList)
        result: List[int] = []
        if cpnLength < rootLength:
            return result
        # 动态规划思想，找根的第 n 笔的切片列表取决于根第 n-1 笔的切片列表。由此反推，先找根第
        # 1笔的切片列表，然后反复依照前一笔的切片列表找下一笔的切片列表，直到根所有笔画查找完毕。
        # 若在查找根的某一笔时切片列表为空，则提前终止，返回空列表。
        validIndexLists: List[List[int]] = [] # 记录当前根笔画的切片列表
        rootFirstStroke = rStrokeList[0]
        lengthLimit = cpnLength - rootLength + 1 # 根的笔画序列长度限制查找范围
        for cpnStrokeIndex in range(0, lengthLimit):
            if cpnStrokeList[cpnStrokeIndex].feature == rootFirstStroke.feature:
                validIndexLists.append([cpnStrokeIndex])
        if len(validIndexLists) == 0: # 根第1笔就已经没有找到切片的话直接返回空列表
            return result
        # 循环查找根的第2笔到末笔的切片列表，每次查找均以上一笔的切片列表为依照
        for rStrokeIndex in range(1, rootLength):
            nextLevelValidIndexLists: List[List[int]] = []
            limit = lengthLimit + rStrokeIndex # 根据查找的是根剩余的长度调整查找范围
            rootTopoRowStr = ' '.join(root.topologyMatrix[rStrokeIndex])
            for indexList in validIndexLists:
                for cpnStrokeIndex in range(indexList[-1]+1, limit):
                    if cpnStrokeList[cpnStrokeIndex].feature == rStrokeList[rStrokeIndex].feature:
                        expandedIndexList = indexList + [cpnStrokeIndex]
                        # 检查拓扑是否符合
                        cTopoRow = component.topologyMatrix[cpnStrokeIndex]
                        tmpTopoStr = ''
                        for i in indexList:
                            tmpTopoStr += cTopoRow[i] + ' '
                        tmpTopoStr = tmpTopoStr.strip()
                        if  tmpTopoStr == rootTopoRowStr:
                            nextLevelValidIndexLists.append(expandedIndexList)
            if len(nextLevelValidIndexLists) == 0:
                return result
            # 每完成根的一个笔画的查找，更新切片列表，用于下一笔的查找
            validIndexLists = nextLevelValidIndexLists
        for indexList in validIndexLists:
            result.append(component.indexListToBinary(indexList))
        return result

    def genScheme(self, component: Component) -> Tuple[Component, ...]:
        '''找出部件在根集中的所有可行组合

        参数:
            component: 待组合的部件

        输出:
            Tuple[int,...]: 最优组合，根用切片二进制数表示
        '''
        binaryDict: Dict[int,Component] = {}
        for root in self.componentRoot.values():
            sliceBinaryList = Sequential.genSliceBinaries(component, root)
            for sliceBinary in sliceBinaryList:
                binaryDict[sliceBinary] = root
        sliceBinaryList = list(binaryDict.keys())
        listLength = len(sliceBinaryList)
        schemeList : List[Tuple[int,...]] = []
        if listLength == 0:
            return schemeList
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
        def combineNext(currentBinary: int, currentCombination: Tuple[int,...]):
            missingBinary = finishBinary - currentBinary
            firstMissingBinary = 2 ** (len(bin(missingBinary)) - 3)
            start = binarySearch(missingBinary)
            end = binarySearch(firstMissingBinary)
            for index in range(start, end+1):
                binary = sliceBinaryList[index]
                if currentBinary & binary == 0:
                    newBinary = currentBinary + binary
                    expandedCombination = currentCombination + (binary,)
                    if newBinary == finishBinary:
                        schemeList.append(expandedCombination)
                    else:
                        combineNext(newBinary, expandedCombination)
        combineNext(0,())
        component.schemeList = schemeList
        schemeBinary = self.selector(component)
        return tuple(map(lambda x: binaryDict[x], schemeBinary))

    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        if component.name in self.componentRoot:
            return (self.componentRoot[component.name],)
        else:
            return self.genScheme(component)

    def _getCompoundScheme(_, compound: Compound) -> Tuple[Component, ...]:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        return firstChild.scheme + secondChild.scheme
