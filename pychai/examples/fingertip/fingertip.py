'''
实现鸽码
'''

from pychai import Sequential, Character, Component, Compound, loadConfig, stdout, stderr
from os.path import join, dirname

class FingerTip(Sequential):
    '''
    叶类
    '''
    def __init__(self, **kwargs):
        d = dirname(__file__)
        self.CONFIG = loadConfig(join(d, 'wubi98.config.yaml'))
        self.STDOUT = stdout(join(d, 'wubi98.result.yaml'))
        self.STDERR = stderr(join(d, 'wubi98.log'))
        super().__init__(**kwargs)

    def _encode(self, character: Character) -> str:
        if isinstance(character, Component):
            scheme = character.scheme[:4]
        else:
            first = character.firstChild
            second = character.secondChild
            if isinstance(first, Component) and isinstance(second, Component):
                scheme = first.scheme[:2] + second.scheme[:2]
            elif isinstance(first, Component) and isinstance(second, Compound):
                scheme = first.scheme[:1] + \
                second.firstChild.scheme[:1] + \
                second.secondChild.scheme[:2]
            elif isinstance(first, Compound) and isinstance(second, Component): # 三分字，前二后一
                scheme = first.firstChild.scheme[:1] + \
                first.secondChild.scheme[:1] + \
                second.scheme[:2]
            else: # 四分字
                assert isinstance(first, Compound)
                assert isinstance(second, Compound)
                scheme = first.firstChild.scheme[:1] + \
                first.secondChild.scheme[:1] + \
                second.firstChild.scheme[:1] + \
                second.secondChild.scheme[:1]
        if len(scheme) < 4: # 末码补全
            scheme = (scheme + (scheme[-1:] * 3))[:4]
        return ''.join([self.rootMap[root.name] for root in scheme])

if __name__ == '__main__':
    fingertip = FingerTip(debug=True)
    fingertip()
