import abc
from typing import Dict, Optional, List
from pychai.data import WEN, ZI
from pychai.data_handler import *
from pychai.classes import Char, UnitChar, NestedChar
import time

class ChaiAbstract():
    def __init__(self, schemaName: str, path: str=''):
        print("初始化拆分对象...")
        start = time.time()
        self.charDict = build_objChar_dict(WEN,ZI)
        schemaData = loadSchemaData(schemaName,path)
        self.schemaInfo: dict = schemaData['schema']
        self.degenerator = build_degenerator(schemaData)
        self.selector = build_selector(schemaData)
        self.storkeClassifier = build_strokeClassifier(schemaData)
        self.rootKeymap, self.degeneracy = generate_rootKeymap_degeneracy(
            schemaData, self.charDict, self.degenerator)
        self.filteredCharNameList = sorted(filter(lambda x: len(x) == 1,
            self.charDict.keys()), key = ord)
        self.schemaResultDict: Optional[Dict[str, str]] = None
        self.keycodeResultDict: Optional[Dict[str, str]] = None
        elapsed = time.time() - start
        print("初始化完毕。耗时：%dms。" % int(elapsed * 1000))

    @abc.abstractmethod
    def genSchemeUnitChar(self, unitChar: UnitChar) -> None:
        pass

    def genSchemeChar(self, char: Char) -> None:
        if not char.scheme:
            if isinstance(char, UnitChar):
                self.genSchemeUnitChar(char)
            elif isinstance(char, NestedChar):
                firstComponentChar = char.firstComponent
                secondComponentChar = char.secondComponent
                self.genSchemeChar(firstComponentChar)
                self.genSchemeChar(secondComponentChar)
                char.scheme = list(firstComponentChar.scheme) + \
                    list(secondComponentChar.scheme)
                if char.thirdComponent:
                    thirdComponentChar = char.thirdComponent
                    self.genSchemeChar(thirdComponentChar)
                    char.scheme += list(thirdComponentChar.scheme)
            else:
                raise TypeError("不能处理该类型")

    @abc.abstractmethod
    def encodeChar(self, char: Char) -> None:
        pass

    def genScheme(self) -> None:
        print("开始拆分...")
        start = time.time()
        if not self.schemaResultDict:
            self.schemaResultDict = {}
        for charName in self.filteredCharNameList:
            char = self.charDict[charName]
            self.genSchemeChar(char)
            self.schemaResultDict[charName] = ''.join([unitChar.name \
                for unitChar in char.scheme])
        elapsed = time.time() - start
        print("拆分完成。耗时：%dms。" % int(elapsed * 1000))

    def encode(self) -> None:
        print("开始编码...")
        start = time.time()
        if not self.keycodeResultDict:
            self.keycodeResultDict = {}
        for charName in self.filteredCharNameList:
            objChar = self.charDict[charName]
            self.encodeChar(objChar)
            self.keycodeResultDict[charName] = objChar.keycode
        elapsed = time.time() - start
        print("编码完成。耗时：%dms。" % int(elapsed * 1000))

    def output(self, directory='', outputSchemaResult=False) -> None:
        schemaId = self.schemaInfo['schema_id']
        version = self.schemaInfo['version']
        resultDict = None
        filename = None
        finishMsg = None
        if not outputSchemaResult:
            resultDict = self.keycodeResultDict
            filename = '%s%s.dict.yaml' % (directory, schemaId)
            finishMsg = "输出编码表完成。"
        else:
            resultDict = self.schemaResultDict
            filename = '%s%s.root.dict.yaml' % (directory, schemaId)
            finishMsg = "输出拆分表完成。"
        if not resultDict:
            raise Exception("未执行拆分或编码")
        with open(filename, 'w', encoding='utf-8') as f: # 写进文件
            f.write('# Chai dictionary: %s\n\n---\nname: %s\n' \
                % (schemaId, schemaId))
            if version:
                f.write('version: %s\n' % version)
            f.write('columns:\n  - text\n  - code\n...\n')
            for charName, result in resultDict.items():
                f.write('%s\t%s\n' % (charName, result))
        print(finishMsg)