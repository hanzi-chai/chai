from unittest import TestCase
from numpy import array
from numpy.linalg import norm
from pychai.base import Stroke, Linear

class TestCurve(TestCase):
    '''
    测试 curve 模块
    '''

    def test_stroke(self):
        data = {'feature': '横折提', 'start': [8, 37], 'curveList': [{'command': 'h', 'parameterList': [20]}, {'command': 'v', 'parameterList': [50]}, {'command': 'l', 'parameterList': [17, -13]}]}
        stroke = Stroke(data)
        self.assertIsInstance(stroke.curveList[2], Linear)
        self.assertAlmostEqual(stroke.linearizeLength, 91.400934559)
