from unittest import TestCase
from numpy import array
from numpy.linalg import norm
from pychai.base import Linear, Cubic

class TestCurve(TestCase):
    '''
    测试 curve 模块
    '''

    def test_linear(self):
        P0 = array([10, 30])
        P1 = array([80, 50])
        linear = Linear(P0, P1)
        self.assertAlmostEqual(norm(linear(0.1) - array([17, 32])), 0)
        self.assertAlmostEqual(norm(linear.derivative()(0.5) - array([70, 20])), 0)
        self.assertAlmostEqual(norm(linear.linearize().P0 - linear.P0), 0)
        self.assertAlmostEqual(linear.linearizeLength(), 72.80109889)

    def test_cubic(self):
        P0 = array([50, 20])
        P1 = array([50, 40])
        P2 = array([30, 60])
        P3 = array([10, 60])
        cubic = Cubic(P0, P1, P2, P3)
        self.assertAlmostEqual(norm(cubic(0.1) - array([49.42, 25.98])), 0)
        self.assertAlmostEqual(norm(cubic.derivative()(0.5) - (cubic(0.50001) - cubic(0.49999)) / 0.00002), 0)
        self.assertAlmostEqual(norm(cubic.linearize().P0 - array([50, 20])), 0)
        self.assertAlmostEqual(cubic.linearizeLength(), 56.568542495)
