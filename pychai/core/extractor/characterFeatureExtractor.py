'''拆分器抽象基类'''
from abc import ABC, abstractmethod
from typing import List

from ...base import Character


class CharacterFeatureExtractor(ABC):
    '''拆分器抽象类'''
    def __init__(self, characters: List[Character]):
        self.characters = characters

    @abstractmethod
    def extract(self):
        '''
        提取码元
        '''
        pass

    @classmethod
    @abstractmethod
    def require(cls):
        '''请求加载的数据'''
        pass
