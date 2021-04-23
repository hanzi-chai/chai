from bisect import bisect_left, bisect_right
from typing import List, Tuple
from .chai import Chai
from ..base import Component, Compound, Character
from ..util import strokeFeatureEqual, findCorner

class Sequential(Chai):
    '''
    经典形码
    '''

    def __init__(self, withCornerInformation=False, **kwargs):
        self.withCornerInformation = withCornerInformation
        super().__init__(**kwargs)

    @staticmethod
    def generateSliceBinaries(component: Component, root: Component) -> List[int]:
        '''
        :param component: 待拆部件
        :param root: 根部件
        :returns: 根部件在待拆部件中的所有有效切片。没有找到切片时返回空列表。

        找出一个字根在一个部件中的所有有效切片。

        例:
        待拆部件「夫」，笔画列表为`['横', '横', '撇', '捺']`，
        其每一位都取用 index 列表表示为`[0, 1, 2, 3]`，二进制表示为0b1111，即十进制数字15。
        根部件「大」，其在「夫」中的有效的切片为「夫」的第1、3、4笔，或第2、3、4笔，
        其二进制表示分别为 0b1011、0b0111，即十进制数字 11、7。
        故输出有效切片集为`[11, 7]`。
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
                    if strokeFeatureEqual(cStroke.feature, rStroke.feature):
                        cStrokeTopo = [component.topologyMatrix[cIndex][i]
                                       for i in indexList]
                        if rStrokeTopo == cStrokeTopo:
                            validFragments.append(indexList + [cIndex])
            if not validFragments: return [] # 缺笔，提前终止
        return [component.indexListToBinary(indexList) for indexList in validFragments]

    def generateScheme(self, component: Component) -> Tuple[Component, ...]:
        '''
        找出部件在根集中的所有可行组合。

        :param component: 待组合的部件
        :returns: 最优拆分组合，根用切片二进制数表示。
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
        schemeBinary = self.selector(component)
        return schemeBinary

    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        if component.name in self.componentRoot:
            return (self.componentRoot[component.name],)
        schemeBinary = self.generateScheme(component)
        scheme = tuple(component.binaryDict[x] for x in schemeBinary)
        if not self.withCornerInformation:
            return scheme
        def findRoot(index):
            binary = 1 << (component.length - index - 1)
            cornerRootBinary, = filter(lambda x: x & binary, schemeBinary)
            root = component.binaryDict[cornerRootBinary]
            return root
        lt, rt, lb, rb = map(findRoot, findCorner(component))
        return {
            'all': scheme,
            'lt': lt,
            'rt': rt,
            'lb': lb,
            'rb': rb
        }

    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        scheme = firstChild.scheme + secondChild.scheme
        if not self.withCornerInformation:
            return scheme
        operator = compound.operator
        lt = firstChild.scheme['lt']
        rt = secondChild.scheme['rt'] if operator in 'hl' else firstChild.scheme['rt']
        lb = secondChild.scheme['lb'] if operator in 'zq' else firstChild.scheme['lb']
        rb = secondChild.scheme['lb'] if operator in 'hz' else firstChild.scheme['lb']
        return {
            'all': scheme,
            'lt': lt,
            'rt': rt,
            'lb': lb,
            'rb': rb
        }

    def _log(self, character: Character) -> None:
        self.STDERR.debug(character)
