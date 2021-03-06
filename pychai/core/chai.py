'''
Chai 基类
'''

from abc import ABC, abstractmethod
from typing import Tuple
from ..base import Character, Component, Compound, Selector
from ..util.load import loadData, loadConfig, loadReference, stdout, stderr
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
        self.COMPONENTS, self.COMPOUNDS = loadData(withTopology=True,withCorner=True)
        '''保存所有部件的名称到部件的映射'''
        '''保存所有复合体的名称到复合体的映射'''
        self.selector: Selector = buildSelector(self.CONFIG)
        self.classifier         = buildClassifier(self.CONFIG)
        self.rootMap            = buildRootMap(self.CONFIG)
        self.componentRoot, self.compoundRoot = buildRoots(self.CONFIG,
            self.COMPONENTS, self.COMPOUNDS)
        if log:
            self.REFERENCE = loadReference(reference)
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

    @abstractmethod
    def _log(self, character: Character) -> None:
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
        for name, character in self.COMPONENTS.items():
            if character.inGB: character.codeList = self._encode(character)
        for name, character in self.COMPOUNDS.items():
            if character.inGB: character.codeList = self._encode(character)

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
        GB = sorted([v.name for k, v in {**self.COMPONENTS, **self.COMPOUNDS}.items() if v.inGB], key=ord)
        for characterName in GB:
            if characterName in self.COMPONENTS:
                character = self.COMPONENTS[characterName]
            elif self.charset == 'GB':
                character = self.COMPOUNDS[characterName]
            else:
                continue
            self.STDOUT.write(f'{characterName}: [{", ".join(character.codeList)}]\n')
            print(character.codeList, self.REFERENCE[character.name])
            if self.STDERR and not all(code in character.codeList for code in self.REFERENCE[character.name]):
                self._log(character)
        self.STDOUT.close()
