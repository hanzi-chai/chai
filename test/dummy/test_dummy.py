from unittest import TestCase
from os.path import dirname, join
from pychai import Character, Sequential, loadConfig, stdout, stderr

class TestDummy(TestCase):
    def test_dummy(self):
        class Dummy(Sequential):
            def __init__(self, **kwargs):
                d = dirname(__file__)
                self.CONFIG = loadConfig(join(d, 'dummy.config.yaml'))
                self.STDOUT = stdout(join(d, 'dummy.result.yaml'))
                self.STDERR = stderr(join(d, 'dummy.log'))
                super().__init__(**kwargs)

            def _encode(self, character: Character) -> str:
                return ''

        dummy = Dummy()
        dummy()
