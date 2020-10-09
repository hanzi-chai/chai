from unittest import TestCase
from pychai.cache.topology import Topology
from pychai.util import loadComponents
from numpy import array, stack
from numpy.linalg import norm

class TestTopology(TestCase):
    def test_basic(self):
        topology = Topology()
        def f(a):
            x, y = a
            return array([2 * x + 3 * y**2 - 5, x + y - 2])
        def J(a):
            x, y = a
            return array([[2, 6 * y], [1, 1]])
        r = array([1.5, 0.5])
        r0 = array([1., 1.])
        topology._newton(f, J, r)
        self.assertAlmostEqual(norm(r - r0), 0, delta=1e-6)

    def test_zhang(self):
        topology = Topology()
        COMPONENTS = loadComponents()
        zhang = COMPONENTS['丈']
        c1 = zhang.strokeList[1].curveList[0]
        c2 = zhang.strokeList[2].curveList[0]
        c1l = c1.linearize()
        c2l = c2.linearize()
        x = topology._linear(c1l, c2l)
        def f(a):
            t1, t2 = a
            return c1(t1) - c2(t2)
        c1p = c1.derivative()
        c2p = c2.derivative()
        def J(a):
            t1, t2 = a
            return stack((
                c1p(t1), -c2p(t2)
            ), axis=1)
        topology._newton(f, J, x)
        t1, t2 = x
