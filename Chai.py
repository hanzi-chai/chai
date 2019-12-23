from tools import *
from preset import *
from tree import Tree
import time


# 基础对象--------------------------------------------------------------------


class Stroke():
    
    """
    笔画对象：
      - 类别（31 种）
      - 控制点列表（2 个至 6 个）
    注：类别和控制点详见
        https://github.com/lanluoxiao/Chai/wiki/1-%E3%80%8C%E6%96%87%E3%80% \
        8D%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83。
    """
    
    def __init__(self, obj):
        self.type = obj[0]
        controlList = []
        for point in obj[1:]:
            controlList.append((int(point[0]), int(point[1])))
        self.controlList = controlList
    
    def __str__(self):
        return str(self.type) + ':' + str(self.controlList) + ' '


class Char():
    
    """
    汉字对象（对象字 objectChar）：
      - 名称（名义字 nameChar）
      - 笔画列表，每个元素是一个 Stroke 对象
    """
    
    def __init__(self, nameChar, strokeList):
        self.name = nameChar
        self.strokeList = strokeList
        self.charlen = len(strokeList)
    
    def __str__(self):
        strokeList = [str(stroke) for stroke in self.strokeList]
        return self.name + '{\n\t' + '\n\t'.join(strokeList) + '\n\t}'

# 方案解析器------------------------------------------------------------------

class Schema:
    
    """
    方案对象：
        - 「文」数据：含控制点笔画列的基础字根
        - 「字」数据：含嵌套结构的字
        - 用户定义方案
        - 解析函数
    """
    
    def __init__(self, schemaName):
        """
        功能：加载基础数据，并加载用户方案（暂定）
        """
        self.__fieldDict = {
            '笔画列表': getStrokeList,
            '笔画拓扑': getTopoList
        } 
        self.__sieveDict = {
            '根少优先': schemeLen,
            '笔顺优先': schemeOrder,
            '取大优先': schemeBias
        }
        self.__wen = loadYAML('文') # 文数据库，即基础字根
        self.__zi = loadYAML('字') # 字数据库，即嵌套表
        self.tree = {}
        for nameChar, expression in self.__zi.items():
            tree = Tree(nameChar, expression, self.__zi)
            self.tree[nameChar] = tree
        allKeys = list(self.__wen.keys()) + list(self.__zi.keys())
        self.charList = sorted(filter(lambda x: len(x) == 1, allKeys), key = ord)
        self.dir = 'preset/%s/' % schemaName
        self.schema = loadYAML('%s.schema' % schemaName, self.dir)
        self.dict = loadYAML('%s.dict' % schemaName, self.dir)
        self.alias = loadYAML('%s.alias' % schemaName, self.dir)
        self.parseDictAndAlias()

    def setField(self, fieldName, field):
        self.__fieldDict[fieldName] = field
    
    def setSieve(self, sieveName, sieve):
        self.__sieveDict[sieveName] = sieve
    
    def genPowerDict(self, objectChar):
        """
        功能：解析出基础字的所有有效切片，构造切片到用户字根的字典 powerDict
        输入：基础字的对象字
        输出：将 powerDict 传给对象字
        备注1：有效切片是由用户定义的字根定义的
        备注2：依赖退化函数 degenerate ，依赖用户字根索引字典 degeneracy
        """
        objectChar.powerDict = {}
        # 生成掩码，二进制分别为 1，10，100……
        l = objectChar.charlen
        mask = [1 << (l-i-1) for i in range(l)]
        for k in range(1, 2**l):
            sliceStrokeList = []
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明某一位为 1
            # 此时添加这一位对应的笔画
            for idx, item in enumerate(mask):
                if k & item:
                    sliceStrokeList.append(objectChar.strokeList[idx])
            characteristicString = self.degenerator(Char('', sliceStrokeList))
            # 找不到退化字根的切片将会标记为None
            objectChar.powerDict[k] = self.degeneracy.get(characteristicString)

    def genSchemeList(self, objectChar):
        """
        功能：解析出在给定字根集下对象字的所有有效的拆分
        输入：对象字（字、字根）
        输出：将所有有效的拆分 schemeList 传给 objectChar
        """
        l = objectChar.charlen
        # 建立一个字典记录拆分状态，若已拆完则为真，否则为假
        uncompletedList = [(2**l - 1, )]
        completedList = []
        # 将拆分列表进行迭代，每次选取未拆完的一个对象，将最后一个组件拆分一次
        while uncompletedList:
            newUncompletedList = []
            for scheme in uncompletedList:
                residue = scheme[-1]
                rootList = list(filter(lambda x: objectChar.powerDict[x],
                                nextRoot(residue)))
                # 上一行：无效切片会因为返回None而被filter筛除
                for root in rootList:
                    if root != residue: # 没拆完
                        newUncompletedList.append(scheme[:-1] + 
                                                (root, residue - root))
                    else: # 新拆出的字根和原有剩余一样大，说明已拆完
                        completedList.append(scheme)
            uncompletedList = newUncompletedList
        objectChar.schemeList = completedList

    def genBestScheme(self, objectChar):
        objectChar.bestScheme = self.selector(objectChar)
    
    def degenerator(self, objectChar):
        characteristicString = ''
        if objectChar.charlen > 1:
            for fieldName in self.schema['degenerator']:
                field = self.__fieldDict[fieldName]
                characteristicString += field(objectChar)
        else:
            characteristicString = objectChar.strokeList[0].type
        return characteristicString

    def selector(self, objectChar):
        for sieveName in self.schema['selector']:
            sieve = self.__sieveDict[sieveName]
            bestEval = min(sieve(objectChar, scheme) for scheme in objectChar.schemeList)
            selectBoolean = lambda scheme: sieve(objectChar, scheme) == bestEval
            objectChar.schemeList = list(filter(selectBoolean, objectChar.schemeList))
        # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
        if len(objectChar.schemeList) == 1:
            return tuple(
                {
                'name': objectChar.powerDict[x], 
                'slice': x
                }
                for x in objectChar.schemeList[0])
        else:
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' % (objectChar.name, objectChar.schemeList))
    
    def parseDictAndAlias(self):
        """
        功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
        输入：基础数据、用户方案（Schema）
        输出：用户字根索引字典 degeneracy 、键位索引字典 rootSet
        """
        # 检查笔画定义是否完整
        lostStrokes = checkCompleteness(self.dict['stroke'])
        if lostStrokes: # 若有缺失定义，发起错误
            raise ValueError('未定义的笔画：%s' % str(lostStrokes))
        else: # 否则，规整数据
            for component in self.alias:
                indexList = self.alias[component][1]
                self.alias[component][1] = expand(indexList) # 展开省略式
        self.rootSet = {} # 字根名到键位的映射，用于取码时键位索引
        self.degeneracy = {} # 退化字根到字根的映射，用于构建powerDict
        for key, rootList in self.dict['map'].items():
            for root in rootList:
                # 是单笔画字根
                if root in self.dict['stroke']:
                    for strokeType in self.dict['stroke'][root]:
                        self.rootSet[strokeType] = key
                        self.degeneracy[strokeType] = strokeType
                # 字根是「文」数据中的一个部件
                elif root in self.__wen:
                    strokeList = [Stroke(stroke)
                                  for stroke in self.__wen[root]]
                    objectChar = Char(root, strokeList)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar.name
                # 字根不是「文」数据库中的部件，但用户定义了它
                elif root in self.alias:
                    source, indexer = self.alias[root]
                    strokeList = [Stroke(self.__wen[source][int(index)])
                                  for index in indexer]
                    objectChar = Char(root, strokeList)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar.name
                # 这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
                elif root in self.__zi:
                    pass

    def run(self):
        """
        功能：解析出文数据库中字按拆分逻辑及用户定义字根拆分出的拆分列
             建立文数据库中字到拆分列的字典
        输入：基础数据、用户方案
        输出：基础字根拆分索引字典component
        """
        """
        嵌套拆分
        输入：字
        输出：计算一个字所依赖的所有其他字（文数据库中的基础字/部件）
        """
        self.component = {}
        self.gpdTime = 0
        self.decTime = 0
        self.selTime = 0
        for nameChar in self.__wen:
            strokeList = [Stroke(stroke) for stroke in self.__wen[nameChar]]
            objectChar = Char(nameChar, strokeList)
            objectChar.bestScheme = None
            time0 = time.time()
            # 取幂集
            self.genPowerDict(objectChar)
            time1 = time.time()
            # 拆分
            self.genSchemeList(objectChar)
            time2 = time.time()
            # 择优
            self.genBestScheme(objectChar)
            time3 = time.time()
            # 将字到拆分列写入映射
            self.component[nameChar] = objectChar.bestScheme
            self.gpdTime += time1 - time0
            self.decTime += time2 - time1
            self.selTime += time3 - time2