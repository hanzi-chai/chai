from typing import List, Callable
from .character import Component

class Selector:
    '''
    选择器
    '''

    def __init__(self, sieveList: List[Callable[[Component], None]]):
        self.sieveList = sieveList

    def __call__(self, component: Component) -> None:
        for sieve in self.sieveList:
            scoreList = [sieve(component, scheme) for scheme in component.schemeList]
            bestScore = min(scoreList)
            component.schemeList = [scheme
                for scheme, score in zip(component.schemeList, scoreList)
                if score == bestScore]
        if len(component.schemeList) == 1:
            # 理论上把字根的二进制表示放进去才完备，但除了 C 输入要用到之外都不用，先不写
            # return tuple(
            #     {
            #         'name': char.powerDict[x],
            #         'slice': x
            #     }
            #     for x in char.schemeList[0])
            component.scheme = tuple(component.powerDict[root] for root in component.schemeList[0])
        else:
            # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' \
                % (component.name, component.schemeList))
