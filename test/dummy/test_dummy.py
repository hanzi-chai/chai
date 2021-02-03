from unittest import TestCase
from os.path import dirname, join
from pychai import Character, Sequential, loadConfig, stdout, stderr

class TestDummy(TestCase):
    def test_dummy(self):
        class Dummy(Sequential):
            def _encode(self, character: Character) -> str:
                return ''

        d = dirname(__file__)
        configPath = join(d, 'dummy.config.yaml')
        resultPath = join(d, 'dummy.result.yaml')
        logPath = join(d, 'dummy.log')
        Dummy(config='dummy.config.yaml', config=configPath, result=resultPath, log=logPath)
