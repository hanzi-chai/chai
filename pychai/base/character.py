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

class Fragment(Component):
    def __init__(self, name: str, strokeList: List[Stroke], source: Component, indexList: List[int]):
        super().__init__(name, strokeList)
        self.source = source
        self.indexList = indexList

class Singlet(Component):
    def __init__(self, name):
        stroke = Stroke({
            'feature': name,
            'start': [],
            'curveList': []
        })
        super().__init__(name, [stroke])

class Compound(Character):
    '''
    复合
    '''
    def __init__(self, name: str, operator: str, firstChild: Character, secondChild: Character, mix: int):
        super().__init__(name, operator)
        self.firstChild = firstChild
        self.secondChild = secondChild
        self.mix = mix
