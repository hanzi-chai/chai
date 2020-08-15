from typing import Sequence,List
from .stroke_class import Stroke
from .typings import NameChar

class Char():
    """
    汉字对象（对象字 objectChar）：
      - 名称（名义字 nameChar）
      - 笔画列表，每个元素是一个 Stroke 对象
    """
    def __init__(self, nameChar: NameChar, strokeList: Sequence[Stroke], sourceName=None, sourceSlice=None):
        self.name: NameChar = nameChar
        self.strokeList = strokeList
        self.charlen = len(strokeList)
        self.sourceName = sourceName
        self.sourceSlice = sourceSlice

    def __str__(self):
        strokeList = [str(stroke) for stroke in self.strokeList]
        return self.name + '{\n\t' + '\n\t'.join(strokeList) + '\n\t}'
