from typing import List, Dict, Tuple
from .object import Stroke

class Character:
    '''
    汉字
    '''
    def __init__(self, name: str, operator: str):
        self.name = name
        self.operator = operator
        self.scheme: Tuple[Component, ...] = ()
        self.code: str = ''

class Component(Character):
    '''
    部件
    '''
    def __init__(self, name: str, strokeList: List[Stroke]):
        super().__init__(name, None)
        self.strokeList = strokeList
        self.topologyMatrix = None
        self.powerDict: Dict[int, Component] = {}
        self.schemeList: List[Tuple[Component]] = {}

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
        return Component(name, strokeList, fragmentTopologyMatrix)

class Singlet(Component):
    def __init__(self, name):
        stroke = Stroke({
            'feature': name,
            'start': [],
            'curveList': []
        })
        super().__init__(name, [stroke], [[]])

class Compound(Character):
    '''
    复合
    '''
    def __init__(self, name: str, operator: str, firstChild: Character, secondChild: Character, mix: int):
        super().__init__(name, operator)
        self.firstChild = firstChild
        self.secondChild = secondChild
        self.mix = mix
