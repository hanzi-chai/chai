from typing import Sequence, List, Optional, Dict, Tuple
from .stroke_class import Stroke

class Char():
    """汉字类

    汉字类用于构建包含了一个汉字中的基本信息的对象。它既可以是书写中用到的正规汉字，也可以是拆分
    中用到的非正式汉字部件。

    属性：
        name: 汉字的名称
        struct: 汉字的结构，如“上下结构”“左右结构”等，独体字应为 None 值。
        strokeList: 汉字的笔画列表。当中每一个元素都是 Stroke 对象，按笔画书写顺序排列。
        scheme: 汉字的拆分结果。
    """
    def __init__(self, name: str, struct: str):
        self.name = name
        self.struct = struct
        self.strokeList: Optional[List[Stroke]] = None
        self.scheme: Optional[Tuple[UnitChar,...]] = None
        # TODO: 新增Root类，去除Char类中的keycode属性
        self.keycode: Optional[str] = None

class NestedChar(Char):
    """嵌套字类，继承 Char 类。

    嵌套字类用于表示 Chai/data/zi.yaml 中汉字。这些汉字可表示为2~3个汉字基本单元，通过常见的
    汉字结构（上下结构等）组成。继承属性见父类。

    属性：
        firstComponent: 嵌套结构的首个组成单元。
        secondComponent: 嵌套结构的第二个组成单元。
        thirdComponent: 嵌套结构的第三个组成单元。若不存在时取 None 值。
    """
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
    """汉字基本单元类，继承 Char 类。

    汉字数本单元类用于表示 Chai/data/wen.yaml 中的汉字基本单元。汉字基本单元，即无法用常规汉
    字结构（上下结构等）进行拆分的最小单元。继承属性见父类。

    属性：
        possibleSchemeList: 记录可能的字根拆分。
        powerDict: 记录基本单元所有可能切片的根字典。形如：{ 切片：根 }
        sourceName, sourceSlice: 后续要改造，先不写
    """
    # TODO: sourceName,sourceSlice属性不应该在此类中，应创建另一个类 UnitCharSlice。
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

# TODO:新增 Root 类，用于表示用户字根。

# TODO:新增 UnitCharSlice 类，用于取切片。