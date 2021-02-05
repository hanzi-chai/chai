from functools import cached_property
from typing import List, Dict
from numpy import array
from numpy import ndarray as Point
from .curve import Curve, Linear, Cubic

class Stroke:
    '''
    笔画是由一段或多段曲线首尾相接组成的几何图形，通常记作 :math:`s`。

    :param data: 数据字典，形式类似于 {feature: 横, start: [0, 0], curveList: [{command: h, parameterList: [10]}]}

    '''
    def __init__(self, data: Dict):
        self.feature: str = data['feature']
        '''笔画的笔形，如横、竖等'''
        self.start: Point = array(data['start'])
        '''笔画的起点'''
        self.curveList: List[Curve] = []
        '''笔画的所有曲线构成的列表'''
        for curveData in data['curveList']:
            curve = self.factory(curveData)
            self.curveList.append(curve)

    def factory(self, curveData):
        command = curveData['command']
        parameterList = curveData['parameterList']
        P0 = self.start
        if command == 'h':
            P1 = P0 + array(parameterList + [0])
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        elif command == 'v':
            P1 = P0 + array([0] + parameterList)
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        elif command == 'l':
            P1 = P0 + array(parameterList)
            curve = Linear(P0, P1)
            self.start = P1
            return curve
        else:
            P1 = P0 + array(parameterList[:2])
            P2 = P0 + array(parameterList[2:4])
            P3 = P0 + array(parameterList[4:])
            curve = Cubic(P0, P1, P2, P3)
            self.start = P3
            return curve

    @cached_property
    def linearizeLength(self):
        '''
        :returns: 笔画所包含的所有曲线的线性长度之和
        '''
        return sum(curve.linearizeLength() for curve in self.curveList)

    def __str__(self):
        return f'{self.feature}: {self.start} -> {self.curveList}'
