from numpy import array
from numpy.linalg import norm
from pychai.base import Linear, Cubic
from math import isclose

def test_linear():
    p0 = array([10, 30])
    p1 = array([80, 50])
    linear = Linear(p0, p1)
    assert isclose(norm(linear(0.1) - array([17, 32])), 0)
    assert isclose(norm(linear.derivative()(0.5) - array([70, 20])), 0)
    assert isclose(norm(linear.linearize().p0 - linear.p0), 0)
    assert isclose(linear.linearizeLength(), 72.80109889)

def test_cubic():
    p0 = array([50, 20])
    p1 = array([50, 40])
    p2 = array([30, 60])
    p3 = array([10, 60])
    cubic = Cubic(p0, p1, p2, p3)
    assert isclose(norm(cubic(0.1) - array([49.42, 25.98])), 0, abs_tol=1e-14)
    assert isclose(norm(cubic.derivative()(0.5) - (cubic(0.50001) - cubic(0.49999)) / 0.00002), 0, abs_tol=1e-4)
    assert isclose(norm(cubic.linearize().p0 - array([50, 20])), 0, abs_tol=1e-4)
    assert isclose(cubic.linearizeLength(), 56.568542495, abs_tol=1e-4)
