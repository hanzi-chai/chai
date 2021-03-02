'''拆分系统功能调用模块'''

from typing import List

from ..base import Character, Component, Compound, Selector
from .extractor import CharacterFeatureExtractor


# TODO: 把 chai 改写成全局调用功能的模块
class Chai():

    def __init__(self,
        characters: List[str],
        extractors: List[CharacterFeatureExtractor],
        encoders):
        self.characters = characters
        self.extractors = extractors
        self.featureMapping

    def extract(self):
        for extractor in self.extractors:
            extractor.extract()

    def encode(self):
        pass

    def saveSchemeFile(self):
        pass

    def saveCodeFile(self):
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
