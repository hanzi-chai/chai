from bisect import bisect_left, bisect_right
from typing import List, Tuple
from .chai import Chai
from ..base import Component, Compound, Character


class Sequential(Chai):
    '''
    经典形码
    '''
    @staticmethod
    def generateSliceBinaries(component: Component, root: Component) -> List[int]:
        '''
        找出一个字根在一个部件中的所有有效切片。
        
        例:
        待拆部件「夫」，笔画列表为['横', '横', '撇', '捺']，
        其每一位都取用 index 列表表示为[0, 1, 2, 3]，二进制表示为 0b1111，即十进制数字15。
        根部件「大」，其在「夫」中的有效的切片为「夫」的第1、3、4笔，或第2、3、4笔，
        其二进制表示分别为 0b1011、0b0111，即十进制数字 11、7。
        故输出有效切片集为 [11, 7]。
        
        Parameters
        ----------
        component : Component，待拆部件
        root : Component，根部件
        
        Returns
        -------
        param : List
        根部件在待拆部件中的所有有效切片。没有找到切片时返回空列表。
        
        '''
        if component.length < root.length: return []
        if root.name == '囗': # 特例
            if component.name == '囱框':
                return [7]
            return []
        # 先找根第 1 笔在待拆部件中的 index 集，然后在各 index 后分别查找第 2 笔的 index 集。
        # 顺序迭代每一笔查找，结果集呈树形生长。
        validFragments = [[]]
        for rIndex, rStroke in enumerate(root.strokeList):
            rStrokeTopo = root.topologyMatrix[rIndex]
            for _ in range(len(validFragments)):
                indexList = validFragments.pop(0)
                start = indexList[-1] + 1 if indexList else 0
                end = component.length - root.length + rIndex + 1
                for cIndex, cStroke in enumerate(component.strokeList[start:end]):
                    if cStroke.featureEqual(rStroke.feature):
                        cStrokeTopo = [component.topologyMatrix[cIndex][i]
                                       for i in indexList]
                        if rStrokeTopo == cStrokeTopo:
                            validFragments.append(indexList + [cIndex])
            if not validFragments: return [] # 缺笔，提前终止
        return [component.indexListToBinary(indexList) for indexList in validFragments]

    def generateScheme(self, component: Component) -> Tuple[Component, ...]:
        '''
        找出部件在根集中的所有可行组合。

        Parameters
        ----------
        component : Component，待组合的部件

        Returns
        -------
        param : Tuple
        最优拆分组合。
        '''
        for root in self.componentRoot.values():
            fragmentBins = Sequential.generateSliceBinaries(component, root)
            for fragmentBin in fragmentBins:
                component.binaryDict[fragmentBin] = root
        totFragmentBins = sorted(component.binaryDict.keys())
        schemeList : List[Tuple[int,...]] = []
        if len(totFragmentBins) == 0:
            return schemeList
        holoBin = 2 ** component.length - 1
        def combineNext(curBin: int, curScheme: Tuple[int,...]):
            resBin = holoBin - curBin
            resBin1st = 2 ** (len(bin(resBin)) - 3)
            start = bisect_left(totFragmentBins, resBin1st)
            end = bisect_right(totFragmentBins, resBin)
            for binary in totFragmentBins[start:end]:
                if curBin & binary == 0:
                    newBin = curBin + binary
                    if newBin == holoBin:
                        schemeList.append(curScheme + (binary,))
                    else:
                        combineNext(newBin, curScheme + (binary,))
        combineNext(0, ())
        component.schemeList = schemeList
        bestScheme = self.selector(component)
        return tuple(component.binaryDict[x] for x in bestScheme)

    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        if component.name in self.componentRoot:
            return (self.componentRoot[component.name],)
        else:
            return self.generateScheme(component)

    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        return firstChild.scheme + secondChild.scheme

    def _log(self, character: Character) -> None:
        self.STDERR.debug(character)
