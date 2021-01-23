from typing import List, Dict, Optional, Tuple
from .stroke import Stroke

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

    :param name:
    '''
    def __init__(self, name: str, strokeList: List[Stroke], topologyMatrix: List[List[str]]):
        super().__init__(name, None)
        self.strokeList                        = strokeList
        self.topologyMatrix                    = topologyMatrix
        self.schemeList: List[Tuple[int, ...]] = []
        self.binaryDict: Dict[int, Component]  = {}

    def indexListToBinary(self, indexList: List[int]):
        '''
        :param indexList: 切片中各笔画在字中的序号
        :returns: 切片的二进制表示
        '''
        length = len(self.strokeList)
        binaryCode: int = 0
        for index in indexList:
            binaryCode += 1 << (length - index - 1)
        return binaryCode

    def fragment(self, name: str, indexList: List[int]):
        '''
        :param name: 字根的名称
        :param indexList: 字根中的各个笔画在源字中的序号
        :returns: 由源字和源字笔画序号列表构建的字根
        '''
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
        return cls(name, [stroke], [[]])

    @property
    def length(self) -> int:
        '''
        :returns: 字的笔画数量
        '''
        return len(self.strokeList)

class Compound(Character):
    '''
    复合字

    :param name: 复合字的名称
    :param operator: 复合字构字的运算符
    :param firstChild: 复合字构字的第一个操作数，可以是部件也可以是复合字
    :param secondChild: 复合字构字的第二个操作数，可以是部件也可以是复合字
    :param mix: 如果第二个操作数的所有笔画并不都在第一个操作数之后，则该整数代表实际书写顺序中，第二个操作数的第一笔是在第一个操作数的第几笔之后开始写的。例如，「区」分解为「匚」和「乂」时，``mix = 1``
    '''
    def __init__(self, name: str, operator: str, firstChild: Character, secondChild: Character, mix: int):
        super().__init__(name, operator)
        self.firstChild  = firstChild
        self.secondChild = secondChild
        self.mix         = mix
