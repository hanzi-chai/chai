from typing import Sequence, List, Optional, Dict, Tuple
from .stroke_class import Stroke

class Char():
    """
    汉字对象（基本部件 unitChar）：
        - 名称（name）
        - 笔画列表，每个元素是一个 Stroke 对象
    """
    def __init__(self, name: str, struct: str):
        self.name = name
        self.struct = struct
        self.strokeList: Optional[List[Stroke]] = None
        self.scheme: Optional[Tuple[UnitChar,...]] = None
        self.keycode: Optional[str] = None

class NestedChar(Char):
    def __init__(self,
        name: str,
        struct: str,
        firstComponent: Char,
        secondComponent: Char,
        thirdComponent: Optional[Char]=None
    ):
        super().__init__(name, struct)
        self.firstComponent = firstComponent
        self.secondComponent = secondComponent
        self.thirdComponent = thirdComponent
        strokeList = firstComponent.strokeList + secondComponent.strokeList
        if thirdComponent:
            strokeList = thirdComponent.strokeList
        self.strokeList = strokeList

class UnitChar(Char):
    def __init__(self,
        name: str,
        strokeList: Sequence[Stroke],
        sourceName: Optional[str]=None,
        sourceSlice: Optional[int]=None
    ):
        super().__init__(name, None)
        self.strokeList = strokeList
        self.sourceName = sourceName
        self.sourceSlice = sourceSlice
        self.possibleSchemeList: Optional[List[List[UnitChar]]] = None
        self.powerDict: Optional[Dict[int,UnitChar]] = None