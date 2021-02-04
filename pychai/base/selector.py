from typing import List, Callable, Tuple
from .character import Component

class Selector:
    '''
    选择器

    :param sieveList: 由筛构成的列表

    >>> selector = Selector(sieveList: List[Callable])
    '''

    def __init__(self, sieveList: List[Callable]):
        self.sieveList = sieveList
        '''由筛构成的列表'''

    def __call__(self, component: Component) -> Tuple[int, ...]:
        '''
        :param component: 已经存储了所有可能拆分方案部件
        :param logger: 用于调试
        :returns: 最优拆分方案对应的二进制表示元组
        '''
        schemeList = component.schemeList.copy()
        infoList = []
        for sieve in self.sieveList:
            scoreList = [sieve(component, scheme) for scheme in schemeList]
            bestScore = min(scoreList)
            infoList.append({
                'name': sieve.__name__,
                'schemeAndScoreList': [(scheme, score) for scheme, score in zip(schemeList, scoreList)]
            })
            schemeList = [scheme
                for scheme, score in zip(schemeList, scoreList)
                if score == bestScore]
        component.infoList = infoList
        if len(schemeList) == 1:
            return schemeList[0]
        else:
            # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' \
                % (component.name, schemeList))
