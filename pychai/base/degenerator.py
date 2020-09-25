'''
退化
'''

from typing import List, Callable
from .character import Component

class Degenerator:
    '''
    退化
    '''

    def __init__(self, fieldList: List[Callable[[Component], str]]):
        self.fieldList = fieldList

    def __call__(self, component: Component) -> str:
        if len(component.strokeList) == 1:
            return component.strokeList[0].feature
        else:
            return tuple(field(component) for field in self.fieldList)
