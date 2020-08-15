"""预置退化映射组件"""
from pychai.data import TOPOLOGY
from pychai.types import Char,Stroke
from typing import Dict


def getStrokeList(objectChar: Char):
    """
    功能：退化函数组件，提取出一个对象字的笔画序列
    输入：对象字
    输出：降维的可散列类对象
    """
    return ' '.join([stroke.type for stroke in objectChar.strokeList])


def getStrokeListSimplified(objectChar: Char, strokeSimplify: Dict[str,str]={
    '竖钩': '竖',
    '竖弯': '竖弯钩',
    '横折钩': '横折',
    '提': '横',
    '捺': '点',
}):
    return ' '.join([strokeSimplify.get(stroke.type, stroke.type) for stroke in objectChar.strokeList])

def getTopoList(objectChar: Char):
    """
    功能：退化函数组件，提取出一个对象字的拓扑
    输入：对象字
    输出：一个 n(n-1)/2 长度的字符串，n 为笔段个数
    """
    if objectChar.sourceName:
        ss = objectChar.sourceSlice
        l = TOPOLOGY[objectChar.sourceName]
        nestedList = [
            [
                relation for nrelation, relation in enumerate(row)
                if (1 << nrelation) & ss
            ]
            for nrow, row in enumerate(l)
            if (1 << nrow) & ss
        ]
    else:
        nestedList = TOPOLOGY[objectChar.name]
    return ' '.join(' '.join(x) for x in nestedList)
