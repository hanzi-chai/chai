from typing import List

from ....base import Character
from . import CharacterFeatureExtractor


# TODO: 改写成调用 Pictorial 完成四角拆分，不再耦合在一起
class CornerCode(CharacterFeatureExtractor):
    '''四角符号拆分器'''
    def __init__(self, characters: List[Character]):
        super().__init__(characters)
        self.pictorialExtractor

    # TODO: 实现方法
    def extract(self):
        pass

    # TODO: 实现方法
    @classmethod
    def require(cls):
        pass

    # component
    # def findRoot(index):
    #     binary = 1 << (component.length - index - 1)
    #     cornerRootBinary, = filter(lambda x: x & binary, schemeBinary)
    #     root = component.binaryDict[cornerRootBinary]
    # lt, rt, lb, rb = map(findRoot, findCorner(component))
    # return {
    #     'all': scheme,
    #     'lt': lt,
    #     'rt': rt,
    #     'lb': lb,
    #     'rb': rb
    # }

    # compound
    # operator = compound.operator
    # lt = firstChild.scheme['lt']
    # rt = secondChild.scheme['rt'] if operator in 'hl' else firstChild.scheme['rt']
    # lb = secondChild.scheme['lb'] if operator in 'zq' else firstChild.scheme['lb']
    # rb = secondChild.scheme['lb'] if operator in 'hz' else firstChild.scheme['lb']
    # return {
    #     'all': scheme,
    #     'lt': lt,
    #     'rt': rt,
    #     'lb': lb,
    #     'rb': rb
    # }

