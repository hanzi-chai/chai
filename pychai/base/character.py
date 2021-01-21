from typing import List, Dict, Optional, Tuple
from .object import Stroke

class Character:
    '''
    汉字
    '''
    def __init__(self, name: str, operator: str):
        self.name                         = name
        self.operator                     = operator
        self.scheme: Tuple[Component,...] = ()
        self.code                         = ''

class Component(Character):
    '''
    部件
    '''
    def __init__(self, name: str, strokeList: List[Stroke], topologyMatrix: List[List[str]]):
        super().__init__(name, None)
        self.strokeList                        = strokeList
        self.topologyMatrix                    = topologyMatrix
        self.schemeList: List[Tuple[int, ...]] = []
        self.binaryDict: Dict[int, Component]  = {}

    def indexListToBinary(self, indexList: List[int]):
        length = len(self.strokeList)
        binaryCode: int = 0
        for index in indexList:
            binaryCode += 1 << (length - index - 1)
        return binaryCode

    def fragment(self, name: str, indexList: List[int]):
        strokeList = [self.strokeList[index] for index in indexList]
        fragmentTopologyMatrix = [
            [
                relation for nrelation, relation in enumerate(row)
                if nrelation in indexList
            ]
            for nrow, row in enumerate(self.topologyMatrix)
            if nrow in indexList
        ]
        component =  Component(name, strokeList, fragmentTopologyMatrix)
        return component

    @classmethod
    def singlet(cls, name: str):
        stroke = Stroke({
            'feature'   : name,
            'start'     : [],
            'curveList' : []
        })
        return cls(name, [stroke], [])

class Compound(Character):
    '''
    复合
    '''
    def __init__(self, name: str, operator: str, firstChild: Character, secondChild: Character, mix: int):
        super().__init__(name, operator)
        self.firstChild  = firstChild
        self.secondChild = secondChild
        self.mix         = mix
