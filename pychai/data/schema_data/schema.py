from typing import Optional,Mapping,Tuple,List,Union,Sequence,Dict
from pychai.types import *
from pychai.data import WEN,ZI
from pychai.core.init_utils import loadData

# TODO: 调整读取schema模块
class Schema():
    """
    方案拆分类，
    """
    def __init__(self,schemaName):
        data = loadData(schemaName)
        self.degenerator: Degenerator = data['degenerator']
        self.selector: Selector = data['selector']
        self.classifier: Classifier = data['classifier']
        self.mapper: Mapper = data['mapper']
        self.aliaser: Aliaser = data['aliaser']
        self.preHandle()

    def preHandle(self):
        """
        功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
        输出：用户字根索引字典 degeneracy 、键位索引字典 rootKeyMap
        """
        self.rootKeyMap: Dict[UserRoot,Key] = {} # 字根名到键位的映射，用于取码时键位索引
        self.degeneracy: Dict[any,Char] = {} # 退化字根到字根的映射，用于构建powerDict
        allRoots = sum([list(x) for x in self.mapper.values()], [])
        self.diff_kou_wei = True if '口' in allRoots and '囗' in allRoots else False
        for key, rootList in self.mapper.items():
            for root in rootList:
                # 是单笔画字根
                if root in self.classifier:
                    for strokeType in self.classifier[root]:
                        self.rootKeyMap[strokeType] = key
                        self.degeneracy[strokeType] = Char(strokeType, [Stroke([strokeType, None])])
                # 字根是「文」数据中的一个部件
                elif root in WEN:
                    strokeList = [Stroke(stroke)
                                    for stroke in WEN[root]]
                    objectChar = Char(root, strokeList)
                    self.rootKeyMap[root] = key
                    characteristicString = degenerator(objectChar)
                    # self.degeneracy[characteristicString] = objectChar.name
                    # 本来以为只需要放一个名义字，但取末笔的时候要用到，故改为对象字
                    # 给这对字根添加额外的区分：
                    if root in '口囗' and self.diff_kou_wei:
                        self.kou_wei_cs = characteristicString
                        characteristicString += root
                    self.degeneracy[characteristicString] = objectChar
                # 字根不是「文」数据库中的部件，但用户定义了它
                elif root in aliaser:
                    source, indexer = self.aliaser[root]
                    l = len(WEN[source])
                    sliceNum = sum(1 << (l - int(index) - 1) for n, index in enumerate(indexer))
                    strokeList = [Stroke(WEN[source][int(index)])
                                    for index in indexer]
                    objectChar = Char(root, strokeList, sourceName=source, sourceSlice=sliceNum)
                    self.rootKeyMap[root] = key
                    characteristicString = degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar
                # 这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
                elif root in ZI:
                    self.complexRootList.append(root)
                    self.rootKeyMap[root] = key
                else:
                    self.rootKeyMap[root] = key


