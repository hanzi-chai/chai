from functools import cached_property
from typing import List, Dict
from numpy import array
from numpy import ndarray as Point
from .curve import Curve, Linear, Cubic
from re import compile as RE

class Stroke:
    '''
    笔画是由一段或多段曲线首尾相接组成的几何图形，通常记作 :math:`s`。

    :param feature: 笔形，如「横」「竖」「横折」「竖折提」等等
    :param svg: 表示整个笔画的 svg 字符串

    '''
    commandSplitter = RE(r'(?<=\d)(?=[hvlc])')

    def __init__(self, feature: str, svg: str):
        self.feature = feature
        '''笔画的笔形，如横、竖等'''
        self.curveList: List[Curve] = []
        '''笔画的所有曲线构成的列表'''
        commandList = self.commandSplitter.split(svg)
        position: Point = array([int(x) for x in commandList.pop(0)[1:].split(' ')])
        for curveString in commandList:
            curve, position = self.factory(position, curveString)
            self.curveList.append(curve)

    def factory(self, position, curveString):
        command = curveString[0]
        parameterList = [int(x) for x in curveString[1:].split(' ')]
        p0 = position
        if command == 'h':
            p1 = p0 + array(parameterList + [0])
            curve = Linear(p0, p1)
            return curve, p1
        elif command == 'v':
            p1 = p0 + array([0] + parameterList)
            curve = Linear(p0, p1)
            return curve, p1
        elif command == 'l':
            p1 = p0 + array(parameterList)
            curve = Linear(p0, p1)
            return curve, p1
        else:
            p1 = p0 + array(parameterList[:2])
            p2 = p0 + array(parameterList[2:4])
            p3 = p0 + array(parameterList[4:])
            curve = Cubic(p0, p1, p2, p3)
            return curve, p3

    @cached_property
    def linearizeLength(self):
        '''
        :returns: 笔画所包含的所有曲线的线性长度之和
        '''
        return sum(curve.linearizeLength() for curve in self.curveList)

    def __str__(self):
        return f'{self.feature}: {self.start} -> {self.curveList}'
