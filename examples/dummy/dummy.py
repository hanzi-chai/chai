from pychai import Character, Sequential

class Dummy(Sequential):
    def _encode(self, character: Character) -> str:
        return ''

Dummy()()
