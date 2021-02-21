'''
实现现代五笔
'''

from typing import List
from pychai import Sequential, Character

class XDWB(Sequential):
    '''
    叶类
    '''

    def _encode(self, character: Character) -> List[str]:
        scheme = character.scheme
        name = character.name
        l = len(scheme)
        if l == 1:
            root = scheme[0]
            # 单根字中的键名字，击四次该键
            if name in '金言心禾土又竹人文目西石米日广廿丁口王之白田水子月木':
                shapeCode = self.rootMap[root.name] * 4
            # 普通成字字根，报户口 + 顺序笔画 + 不足补音
            else:
                shapeCode = self.rootMap[root.name] + ''.join([self.rootMap[stroke.feature] for stroke in root.strokeList[:3]])
        elif l == 2:
            shapeCode = ''.join([self.rootMap[root.name] for root in scheme])
        else:
            shapeCode = ''.join([self.rootMap[root.name] for root in (scheme[:2] + scheme[-1:])])
        if len(shapeCode) < 4:
            codeList = [shapeCode + initial for initial in character.initialList]
        else:
            codeList = [shapeCode]
        return codeList

XDWB(
    charset='test',
    config='xdwb.config.yaml',
    result='xdwb.result.yaml',
    # log='xdwb.log',
    # reference='xdwb.dict.yaml'
)()
