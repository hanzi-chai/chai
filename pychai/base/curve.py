'''
# 基础（`pychai.base`）

本节介绍了汉字自动拆分系统中用到的基础组件，这些组件以类的形式体现。
'''

from abc import ABC
from typing import List, Dict
from numpy import array
from numpy.linalg import norm

class Curve(ABC):
    '''
    曲线
    '''
    pass

class Linear(Curve):
    '''
    '''

    def __init__(self, P0, P1):
        self.P0 = P0
        self.P1 = P1

    def __call__(self, t):
        return (1 - t) * self.P0 + t * self.P1

    def derivative(self):
        def f(t):
            return self.P1 - self.P0
        return f

    def linearize(self):
        return self

    def linearizeLength(self):
        return norm(self.P1 - self.P0)

    def __str__(self):
        return f'Linear: {self.P0} -> {self.P1}'

class Cubic(Curve):
    '''
    三次 Bezier 曲线的形式为：

    $$
    r_3(t) = (1-t)^3P_1 + 3(1-t)^2tP_2 + 3(1-t)t^2P_3 + t^3P_4
    $$
    '''
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

    def linearizeLength(self):
        return self.linearize().linearizeLength()

    def __str__(self):
        return f'Cubic: {self.P0} -> {self.P1} -> {self.P2} -> {self.P3}'
