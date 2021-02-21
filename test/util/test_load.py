from pychai import loadData
from os.path import join, dirname

def test_loadData():
    loadData(withTopology=True, withCorner=True)
