from pychai import Stroke, Linear

def test_stroke():
    stroke = Stroke('横折提', 'M8 37h20v50l17 -13')
    assert isinstance(stroke.curveList[2], Linear)
    assert abs(stroke.linearizeLength - 91.400934559) < 0.01
