from numpy import array
from pychai.util import findCorner, isNearThan, findCriticalPoints, loadComponents

COMPONENTS = loadComponents()

def test_isNearThan():
    p0 = array([0, 0])
    assert not isNearThan(array([10, 20]), array([20, 10]), p0)
    assert isNearThan(array([10, 10]), array([20, 20]), p0)

def test_findCriticalPoints():
    日 = COMPONENTS['日']
    criticalPointList, fromStroke = findCriticalPoints(日)
    assert len(criticalPointList) == 6

def test_findCorner():
    天 = COMPONENTS['天']
    assert findCorner(天) == (0, 0, 2, 3)
    日 = COMPONENTS['日']
    assert findCorner(日) == (0, 1, 0, 1)
    木 = COMPONENTS['木']
    assert findCorner(木) == (1, 1, 1, 1)
