'''
Chai 基类
'''

import abc
from typing import Tuple
from ..base import Character, Component, Compound, Degenerator, Selector
from ..util import loadGB, loadComponentsWithTopology, loadCompounds, loadConfig
from ..util import buildDegenerator, buildSelector, buildClassifier, buildRootMap, buildDegeneracy
import time

class Chai:
    '''
    抽象基类
    '''

    def __init__(self, configPath):
        self.GB = loadGB()
        self.COMPONENTS = loadComponentsWithTopology()
        self.COMPOUNDS = loadCompounds(self.COMPONENTS)
        self.CONFIG = loadConfig(configPath)
        self.degenerator: Degenerator = buildDegenerator(self.CONFIG)
        self.selector: Selector = buildSelector(self.CONFIG)
        self.classifier = buildClassifier(self.CONFIG)
        self.rootMap = buildRootMap(self.CONFIG)
        self.rootList, self.compoundRootList = buildDegeneracy(self.CONFIG,
            self.COMPONENTS, self.COMPOUNDS)

    @abc.abstractmethod
    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        pass

    @abc.abstractmethod
    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        pass

    @abc.abstractmethod
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

    def chai(self, fileName) -> None:
        t0 = time.time()
        self.getComponentScheme()
        t1 = time.time()
        self.getCompoundScheme()
        t2 = time.time()
        self.encode()
        t3 = time.time()
        print(t1 - t0, t2 - t1, t3 - t2)
        with open(fileName, 'w') as f:
            for characterName in self.GB:
                if characterName in self.COMPONENTS:
                    character = self.COMPONENTS[characterName]
                else:
                    character = self.COMPOUNDS[characterName]
                f.write('%s\t%s\n' % (characterName, character.code))
