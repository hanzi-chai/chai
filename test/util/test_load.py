from unittest import TestCase
from pychai.util import *
from os.path import join, dirname

class TestLoadBuild(TestCase):
    '''
    测试导入
    '''
    def test_all(self):
        GB = loadGB()
        COMPONENTS = loadComponents(withTopology=True, withCorner=True)
        COMPOUNDS = loadCompounds(COMPONENTS)
        CONFIG = loadConfig(join(dirname(__file__), '../dummy/dummy.config.yaml'))
        selector = buildSelector(CONFIG)
        storkeClassifier = buildClassifier(CONFIG)
        rootMap = buildRootMap(CONFIG)
        componentRoot, compoundRoot = buildRoots(CONFIG, COMPONENTS, COMPOUNDS)
