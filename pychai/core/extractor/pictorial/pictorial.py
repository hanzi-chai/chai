'''字形拆分'''
from bisect import bisect_left, bisect_right
from typing import Callable, Dict, List, Tuple, Union

from ....base.character import Character, Component, Compound
from ....loader.load import (loadComponentsDependencies,
                             loadCompoundsDependencies)
from ..characterFeatureExtractor import CharacterFeatureExtractor


class Pictorial(CharacterFeatureExtractor):
    '''字根拆分器'''

    def __init__(self,
        components: List[Component],
        compounds: List[Compound],
        componentRoots: List[Component],
        compoundRoots: List[Compound],
        evaluators: Callable[[Component, Tuple[int, ...]],Union[int,Tuple[int, ...]]]):
        self.components = components
        self.compounds = compounds
        self.componentRoots = componentRoots
        self.compoundRoots = compoundRoots
        self.evaluators = evaluators

    # TODO: 这个函数不知道放在什么模块好，暂时放在这里，后期可能需要配合 classifier 作改动
    @staticmethod
    def strokeFeatureEqual(strokeFeature1: str, strokeFeature2: str):
        '''笔画类型比对，相同为`True`，不相同为`False`。其中`'点'`和`'捺'`视为相同。
        '''
        if strokeFeature1 != strokeFeature2:
            if strokeFeature1 == '点':
                return strokeFeature2 == '捺'
            elif strokeFeature1 == '捺':
                return strokeFeature2 == '点'
            return False
        return True

    @staticmethod
    def generateSliceBinaries(component: Component, root: Component) -> List[int]:
        '''找出一个字根在一个部件中的所有有效切片。

        例: 待拆部件「夫」，笔画列表为`['横', '横', '撇', '捺']`，
        其每一位都取用 index 列表表示为`[0, 1, 2, 3]`，二进制表示为0b1111，即十进制数字15。
        根部件「大」，其在「夫」中的有效的切片为「夫」的第1、3、4笔，或第2、3、4笔，
        其二进制表示分别为 0b1011、0b0111，即十进制数字 11、7。
        故输出有效切片集为`[11, 7]`。

        :param component: 待拆部件
        :param root: 根部件
        :return: 根部件在待拆部件中的所有有效切片。没有找到切片时返回空列表。
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
            end = component.length - root.length + rIndex + 1
            for _ in range(len(validFragments)):
                indexList = validFragments.pop(0)
                start = indexList[-1] + 1 if indexList else 0
                searchField = component.strokeList[start:end]
                for cIndex, cStroke in enumerate(searchField, start):
                    if Pictorial.strokeFeatureEqual(cStroke.feature, rStroke.feature):
                        cStrokeTopo = [component.topologyMatrix[cIndex][i]
                                       for i in indexList]
                        if rStrokeTopo == cStrokeTopo:
                            validFragments.append(indexList + [cIndex])
            if not validFragments: return [] # 缺笔，提前终止
        return [component.indexListToBinary(indexList) for indexList in validFragments]

    def select(self, component: Component) -> Tuple[int, ...]:
        '''
        :param component: 已经存储了所有可能拆分方案部件
        :return: 最优拆分方案对应的二进制表示元组
        '''
        schemeList = component.schemeList
        for evaluator in self.evaluators:
            scoreList = [evaluator(component, scheme) for scheme in schemeList]
            bestScore = min(scoreList)
            schemeList = [scheme
                for scheme, score in zip(schemeList, scoreList)
                if score == bestScore]
        if len(schemeList) == 1:
            return schemeList[0]
        else:
            # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' \
                % (component.name, schemeList))

    def generateComponentSchemeBinary(self, component: Component):
        '''
        找出部件在根集中的所有可行组合。

        :param component: 待组合的部件
        :return: 最优拆分组合，根用切片二进制数表示。
        '''
        for root in self.componentRoots:
            fragmentBins = Pictorial.generateSliceBinaries(component, root)
            for fragmentBin in fragmentBins:
                component.binaryDict[fragmentBin] = root
        totFragmentBins = sorted(component.binaryDict.keys())
        schemeList : List[Tuple[int,...]] = []
        if len(totFragmentBins) == 0:
            return schemeList
        holoBin = 2 ** component.length - 1
        def combineNext(curBin: int, curScheme: Tuple[int,...]):
            restBin = holoBin - curBin
            restBin1st = 2 ** (len(bin(restBin)) - 3)
            start = bisect_left(totFragmentBins, restBin1st)
            end = bisect_right(totFragmentBins, restBin)
            for binary in totFragmentBins[start:end]:
                if curBin & binary == 0:
                    newBin = curBin + binary
                    if newBin == holoBin:
                        schemeList.append(curScheme + (binary,))
                    else:
                        combineNext(newBin, curScheme + (binary,))
        combineNext(0, ())
        component.schemeList = schemeList
        return self.select(component)

    def generateComponentScheme(self, component: Component):
        if component.name in self.componentRoots:
            return (component,)
        schemeBinary = self.generateComponentSchemeBinary(component)
        return tuple(component.binaryDict[x] for x in schemeBinary)

    def generateCompoundScheme(self, compound: Compound):
        return compound.firstChild.scheme + compound.secondChild.scheme

    def extract(self):
        for component in self.components:
            component.scheme = self.generateComponentScheme(component)
        for compound in self.compounds:
            compound.scheme = self.generateCompoundScheme()

    # TODO: 实现方法
    @classmethod
    def require(cls):
        pass
