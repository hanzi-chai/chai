'''拆分系统功能调用模块'''

from abc import ABC, abstractmethod
from typing import Tuple

from ..base import Character, Component, Compound, Selector


# TODO: 把 chai 改写成全局调用功能的模块
class Chai(ABC):
    '''
    抽象基类
    '''
    def __init__(self, characters, extractors, encoders, config='config.yaml', result='result.yaml'):
        self.characters: list[str]
        self.featureExtractors: list
        self.featureMapping

    def extract(self):
        pass

    def encode(self):
        pass

    def output(self):
        pass

    def run(self):
        pass

        # '''
        # 将所有 ``self.GB`` 中汉字的编码写入 ``self.STDOUT``
        # '''
        # GB = sorted([v.name for k, v in {**self.COMPONENTS, **self.COMPOUNDS}.items() if v.inGB], key=ord)
        # for characterName in GB:
        #     if characterName in self.COMPONENTS:
        #         character = self.COMPONENTS[characterName]
        #     elif self.charset == 'GB':
        #         character = self.COMPOUNDS[characterName]
        #     else:
        #         continue
        #     for code in character.codeList:
        #         self.STDOUT.write('%s\t%s\n' % (characterName, code))
        #     if self.STDERR and character.codeList != self.REFERENCE[character.name]:
        #         self._log(character)
        # self.STDOUT.close()
