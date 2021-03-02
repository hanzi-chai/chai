'''图像曲线对象模块'''
from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from numpy import array
from numpy import ndarray as Point
from numpy.linalg import norm


class Curve(ABC):
    '''
    二维参数曲线基类
    '''

    @abstractmethod
    def __call__(self, t: float) -> Point:
        '''
        :param t: 参数
        :return: 该参数下点的取值

        '''
        pass

    @abstractmethod
    def derivative(self) -> Callable:
        '''
        :return: 参数曲线的导函数

        '''
        pass

    @abstractmethod
    def linearize(self):
        '''
        :return: 参数曲线的首尾两个点所确定的一次参数曲线

        '''
        pass

    @abstractmethod
    def linearizeLength(self) -> float:
        '''
        :return: 参数曲线的首尾两个点之间的距离，也即其线性长度

        '''
        pass

class Linear(Curve):
    r'''
    一次 Bezier 曲线（即直线）的形式为：

    .. math::
       \r_1(t)=(1-t)\p_1+t\p_2

    它的几何直观是：\ :math:`t=0` 时，函数位于 :math:`\P_1` 处，而
    :math:`t=1` 时，函数位于 :math:`\P_2` 处，且它是连接 :math:`\P_1,\P_2`
    的一条直线。

    :param p0: 一次 Bezier 曲线的起点
    :param p1: 一次 Bezier 曲线的终点

    从起点和终点构造一次 Bezier 曲线
    '''

    def __init__(self, p0: Point, p1: Point):
        self.p0 = p0
        self.p1 = p1
        self.start = p0
        self.end = p1

    def __call__(self, t: float) -> Point:
        return (1 - t) * self.p0 + t * self.p1

    def derivative(self) -> Callable:
        def f(t):
            return self.p1 - self.p0
        return f

    def linearize(self):
        return self

    def linearizeLength(self):
        return norm(self.p1 - self.p0)

    def __str__(self):
        return f'Linear: {self.P0} -> {self.P1}'

class Cubic(Curve):
    r'''
    三次 Bezier 曲线的形式为：

    .. math::
       \r_3(t) = (1-t)^3\p_1 + 3(1-t)^2t\p_2 + 3(1-t)t^2\p_3 + t^3\p_4

    :param p0: 三次 Bezier 曲线的起点
    :param p1: 三次 Bezier 曲线的第一控制点
    :param p2: 三次 Bezier 曲线的第二控制点
    :param p1: 三次 Bezier 曲线的终点

    从起点和终点构造一次 Bezier 曲线
    '''
    def __init__(self, p0: Point, p1: Point, p2: Point, p3: Point):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.start = p0
        self.end = p3

    def __call__(self, t: float) -> Point:
        return (1 - t)**3 * self.p0 + 3 * (1 - t)**2 * t * self.p1 + 3 * (1 - t) * t**2 * self.p2 + t**3 * self.p3

    def derivative(self) -> Callable[[float], Point]:
        def f(t):
            return 3 * (
                (1 - t)**2 * (self.p1 - self.p0) +
                2 * t * (1 - t) * (self.p2 - self.p1) +
                t**2 * (self.p3 - self.p2)
            )
        return f

    def linearize(self):
        return Linear(self.p0, self.p3)

    def linearizeLength(self) -> float:
        return self.linearize().linearizeLength()

    def __str__(self):
        return f'Cubic: {self.P0} -> {self.P1} -> {self.P2} -> {self.P3}'
