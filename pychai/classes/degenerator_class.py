from .char_class import UnitChar
from typing import Dict, Callable

class Degenerator():
    def __init__(self, fields: Dict[str, Callable[[UnitChar], str]]={}):
        self.fields = fields

    def __call__(self, unitChar: UnitChar) -> str:
        characteristicString = ''
        if len(unitChar.strokeList) > 1:
            for _callable in self.fields.values():
                characteristicString += _callable(unitChar)
        else:
            characteristicString = unitChar.strokeList[0].type
        return characteristicString