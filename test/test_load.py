from unittest import TestCase
from pychai.util import *

class TestLoadBuild(TestCase):
    '''
    测试导入
    '''
    def test_all(self):
        GB = loadGB()
        COMPONENTS = loadComponents()
        COMPOUNDS = loadCompounds(COMPONENTS)
        CONFIG = loadConfig('templates/wubi98/wubi98.config.yaml')
        degenerator = buildDegenerator(CONFIG)
        selector = buildSelector(CONFIG)
        storkeClassifier = buildClassifier(CONFIG)
        rootMap = buildRootMap(CONFIG)
        compoundRootList, degeneracy = buildDegeneracy(CONFIG, degenerator, 
            COMPONENTS, COMPOUNDS)