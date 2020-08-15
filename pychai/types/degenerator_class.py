from .char_class import Char
class Degenerator():
    def __init__(self,fields: List[Callable[[Char],str]]):
        self.fields=fields

    def __call__(self,objectChar: Char)->str:
        characteristicString = ''
        if objectChar.charlen > 1:
            for field in self.fields:
                characteristicString += field(objectChar)
        else:
            characteristicString = objectChar.strokeList[0].type
        return characteristicString