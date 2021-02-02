'''
经典形码
'''
from bisect import bisect_left, bisect_right
from typing import List, Tuple
from collections import deque
from .chai import Chai
from ..base import Component, Compound
from ..util import strokeFeatureEqual

class Sequential(Chai):
    '''
    经典形码
    '''

    @staticmethod
    def generateSliceBinaries(component: Component, root: Component) -> List[int]:
        '''
        :param component: 待拆部件
        :param root: 根部件
        :returns: 根部件在待拆部件中的所有有效切片，切片用二进制表示。没有找到切片时返回空列表。

        找出一个字根在一个部件中的所有有效切片。例: 待拆部件“天”，根部件“大”。“大”在“天”中的有效的切片为“天”的第2、3、4笔。“天” 的笔画列表为['横', '横', '撇', '捺']，每一位都取用 index 列表表示为[0,1,2,3]，二进制表示为 0b1111，只取后三笔用 index 列表表示为[1,2,3]，二进制表示为 0b0111，即整型数字 7 。故输出为 [7]。
        '''
        if component.length < root.length: return []
        if root.name == '囗':
            if component.name == '囱框':
                return [7]
            else:
                return []
        # 动态规划：先找根第 1 笔的切片列表，然后反复依照前一笔的切片列表找下一笔的切片列表，直到根所有笔画查找完毕。
        # 若在查找根的某一笔时切片列表为空，则提前终止，返回空列表。
        validIndexListQueue: deque = deque([[]])
        for rootStrokeIndex in range(root.length):
            rootStrokeFeature = root.strokeList[rootStrokeIndex].feature
            rootTopoRowStr = ' '.join(root.topologyMatrix[rootStrokeIndex])
            for _ in range(len(validIndexListQueue)):
                indexList = validIndexListQueue.popleft()
                startAt = indexList[-1] + 1 if indexList else 0
                endAt = component.length - root.length + 1 + rootStrokeIndex
                for componentStrokeIndex in range(startAt, endAt):
                    if strokeFeatureEqual(component.strokeList[componentStrokeIndex].feature, rootStrokeFeature):
                        expandedIndexList = indexList + [componentStrokeIndex]
                        # 检查拓扑是否符合
                        cTopoRow = component.topologyMatrix[componentStrokeIndex]
                        cpnTopoStr = ' '.join([cTopoRow[i] for i in indexList])
                        if cpnTopoStr == rootTopoRowStr: validIndexListQueue.append(expandedIndexList)
            if not validIndexListQueue: return []
        return [component.indexListToBinary(indexList) for indexList in validIndexListQueue]

    def generateScheme(self, component: Component) -> Tuple[Component, ...]:
        '''
        找出部件在根集中的所有可行组合

        :param component: 待组合的部件
        :returns: 最优组合，根用切片二进制数表示
        '''
        for root in self.componentRoot.values():
            sliceBinaryList = Sequential.generateSliceBinaries(component, root)
            for sliceBinary in sliceBinaryList:
                component.binaryDict[sliceBinary] = root
        sliceBinaryList = list(component.binaryDict.keys())
        listLength = len(sliceBinaryList)
        schemeList : List[Tuple[int,...]] = []
        if listLength == 0:
            return schemeList
        self.STDERR.debug(f'{component.name}')
        self.STDERR.debug(component.binaryDict)
        sliceBinaryList.sort()
        finishBinary = 2 ** component.length - 1
        def combineNext(currentBinary: int, currentCombination: Tuple[int,...]):
            missingBinary = finishBinary - currentBinary
            firstMissingBinary = 2 ** (len(bin(missingBinary)) - 3)
            start = bisect_left(sliceBinaryList, firstMissingBinary)
            end = bisect_right(sliceBinaryList, missingBinary)
            for index in range(start, end):
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
        schemeBinary = self.selector(component, self.STDERR)
        return tuple(map(lambda x: component.binaryDict[x], schemeBinary))

    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        if component.name in self.componentRoot:
            return (self.componentRoot[component.name],)
        else:
            return self.generateScheme(component)

    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        return firstChild.scheme + secondChild.scheme
