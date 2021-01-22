'''
Chai 基类
'''

from abc import ABC, abstractmethod
from typing import Tuple
from ..base import Character, Component, Compound, Selector
from ..util.load import loadGB, loadComponentsWithTopology, loadCompounds, loadConfig
from ..util.build import buildSelector, buildClassifier, buildRootMap, buildRoots, buildRoots
from ..logger import BinaryDictFormatter
import time

class Chai(ABC):
    '''
    抽象基类
    '''


    def __init__(self, debug=False):
        if debug: self.STDERR.setLevel(10)
        self.GB                 = loadGB()
        self.COMPONENTS         = loadComponentsWithTopology()
        self.COMPOUNDS          = loadCompounds(self.COMPONENTS)
        self.selector: Selector = buildSelector(self.CONFIG)
        self.classifier         = buildClassifier(self.CONFIG)
        self.rootMap            = buildRootMap(self.CONFIG)
        self.componentRoot, self.compoundRoot = buildRoots(self.CONFIG,
            self.COMPONENTS, self.COMPOUNDS)

    @abstractmethod
    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        pass

    @abstractmethod
    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        pass

    @abstractmethod
    def _encode(self, character: Character) -> str:
        pass

    def getComponentScheme(self) -> None:
        for component in self.COMPONENTS.values():
            component.scheme = self._getComponentScheme(component)

    def getCompoundScheme(self) -> None:
        for compound in self.COMPOUNDS.values():
            compound.scheme = self._getCompoundScheme(compound)

    def encode(self) -> None:
        for characterName in self.GB:
            if characterName in self.COMPONENTS:
                character = self.COMPONENTS[characterName]
            else:
                character = self.COMPOUNDS[characterName]
            character.code = self._encode(character)

    def __call__(self) -> None:
        t0 = time.time()
        self.getComponentScheme()
        t1 = time.time()
        self.getCompoundScheme()
        t2 = time.time()
        self.encode()
        t3 = time.time()
        for characterName in self.GB:
            if characterName in self.COMPONENTS:
                character = self.COMPONENTS[characterName]
            else:
                character = self.COMPOUNDS[characterName]
            self.STDOUT.write('%s\t%s\n' % (characterName, character.code))
        self.STDOUT.close()
