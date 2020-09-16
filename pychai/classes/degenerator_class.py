from .char_class import UnitChar
from typing import Dict, Callable

class Degenerator():
    """退化器类，用于把汉字基本单元退化为其它表示形式。

    退化器可储存退化函数，自身为可调用。当调用时会执行 __call__方法，依次对汉字基本单元执行自身
    属性中包含的退化函数。

    属性：
        fields: 退化函数字典。形如：{ 退化函数名：退化函数 }。其中退化函数都是接受参数为
        UnitChar 的函数（或可调用对象）。
    """
    def __init__(self, fields: Dict[str, Callable[[UnitChar], str]]={}):
        self.fields = fields

    def __call__(self, unitChar: UnitChar) -> str:
        characteristicString = ''
        if len(unitChar.strokeList) > 1:
            for _callable in self.fields.values():
                characteristicString += _callable(unitChar)
        else:
            characteristicString = unitChar.strokeList[0].type
        return characteristicString