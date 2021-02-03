'''
Chai 基类
'''

from abc import ABC, abstractmethod
from typing import Tuple
from ..base import Character, Component, Compound, Selector
from ..util.load import loadGB, loadComponents, loadCompounds, loadConfig, stdout, stderr, loadExternal
from ..util.build import buildSelector, buildClassifier, buildRootMap, buildRoots
import time

class Chai(ABC):
    '''
    抽象基类
    '''

    def __init__(self, charset='GB', config='config.yaml', result='result.yaml', log=None, reference='dict.yaml'):
        self.charset = charset
        self.CONFIG = loadConfig(config)
        self.STDOUT = stdout(result)
        self.GB                 = loadGB()
        '''保存 GB 字集'''
        self.COMPONENTS         = loadComponents(withTopology=True)
        '''保存所有部件的名称到部件的映射'''
        self.COMPOUNDS          = loadCompounds(self.COMPONENTS)
        '''保存所有复合体的名称到复合体的映射'''
        self.selector: Selector = buildSelector(self.CONFIG)
        self.classifier         = buildClassifier(self.CONFIG)
        self.rootMap            = buildRootMap(self.CONFIG)
        self.componentRoot, self.compoundRoot = buildRoots(self.CONFIG,
            self.COMPONENTS, self.COMPOUNDS)
        if log:
            self.REFERENCE = loadExternal(reference)
            self.STDERR = stderr(log)
            self.STDERR.setLevel(10)
        else:
            self.REFERENCE = self.STDERR = None

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
        '''
        向所有 ``self.COMPONENTS`` 中的部件注入拆分方案
        '''
        for component in self.COMPONENTS.values():
            component.scheme = self._getComponentScheme(component)

    def getCompoundScheme(self) -> None:
        '''
        向所有 ``self.COMPOUNDS`` 中的部件注入拆分方案
        '''
        for compound in self.COMPOUNDS.values():
            compound.scheme = self._getCompoundScheme(compound)

    def encode(self) -> None:
        '''
        向所有 ``self.GB`` 中的汉字注入编码
        '''
        for characterName in self.GB:
            if characterName in self.COMPONENTS:
                character = self.COMPONENTS[characterName]
            else:
                character = self.COMPOUNDS[characterName]
            character.code = self._encode(character)

    def __call__(self) -> None:
        '''
        将所有 ``self.GB`` 中汉字的编码写入 ``self.STDOUT``
        '''
        t0 = time.time()
        self.getComponentScheme()
        t1 = time.time()
        self.getCompoundScheme()
        t2 = time.time()
        self.encode()
        t3 = time.time()
        if self.charset == 'test':
            for characterName in self.GB:
                if characterName in self.COMPONENTS:
                    character = self.COMPONENTS[characterName]
                    self.STDOUT.write('%s\t%s\n' % (characterName, character.code))
                    if self.STDERR and character.code != self.REFERENCE[character.name]:
                        self._log(character)
            self.STDOUT.close()
        else:
            for characterName in self.GB:
                if characterName in self.COMPONENTS:
                    character = self.COMPONENTS[characterName]
                else:
                    character = self.COMPOUNDS[characterName]
                self.STDOUT.write('%s\t%s\n' % (characterName, character.code))
                if self.STDERR and character.code != self.REFERENCE[character.name]:
                    self._log(character)
            self.STDOUT.close()
