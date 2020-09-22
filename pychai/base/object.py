'''
定义数学对象，包括曲线和笔画
'''

from abc import abstractmethod
from typing import List, Dict
from numpy import array

class Curve:
    '''
    曲线
    '''
    @abstractmethod
    def __init__(self, data: Dict):
        pass

class Linear(Curve):
    def __init__(self, P0, P1):
        self.P0 = P0
        self.P1 = P1

    def __call__(self, t):
        return (1 - t) * self.P0 + t * self.P1

    def linearize(self):
        return self

    def derivative(self):
        def f(t):
            return self.P1 - self.P0
        return f

    def __str__(self):
        return f'{self.P0} -> {self.P1}'

class Cubic(Curve):
    def __init__(self, P0, P1, P2, P3):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3

    def __call__(self, t):
        return (1 - t)**3 * self.P0 + 3 * (1 - t)**2 * t * self.P1 + 3 * (1 - t) * t**2 * self.P2 + t**3 * self.P3

    def derivative(self):
        def f(t):
            return 3 * (
                (1 - t)**2 * (self.P1 - self.P0) +
                2 * t * (1 - t) * (self.P2 - self.P1) +
                t**2 * (self.P3 - self.P2)
            )
        return f

    def linearize(self):
        return Linear(self.P0, self.P3)

class Stroke:
    '''
    笔画
    '''
    def __init__(self, data: Dict):
        self.feature: str = data['feature']
        self.start: array = array(data['start'])
        self.curveList: List[Curve] = []
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

    def __str__(self):
        return f'{self.feature}: {self.start} -> {self.curveList}'
