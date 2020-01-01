from .tools import *
from .presets import *
from .objects import *
import time

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
        self.name = schemaName
        self.__fieldDict = {
            '笔画序列': getStrokeList,
            '笔画序列（简）': getStrokeListSimplified,
            '笔画拓扑': getTopoList
        } 
        self.__sieveDict = {
            '根少优先': schemeLen,
            '笔顺优先': schemeOrder,
            '能连不交、能散不连': schemeTopo,
            '取大优先': schemeBias
        }
        self.wen = loadFromPackage('wen.yaml') # 文数据库，即基础字根
        self.zi = loadFromPackage('zi.yaml') # 字数据库，即嵌套表
        # self.zi = {}
        # self.yuan = loadFromPackage('元.yaml') # 元数据库，即预置字根
        self.tree = {}
        self.complexRootList = []
        for nameChar, expression in self.zi.items():
            tree = Tree(nameChar, expression, self.zi)
            self.tree[nameChar] = tree
        allKeys = list(self.wen.keys()) + list(self.zi.keys())
        self.charList = sorted(filter(lambda x: len(x) == 1, allKeys), key = ord)
        self.encoder = {}
        try:
            self.schema = load('%s.schema.yaml' % self.name, withNumbers=False)
        except FileNotFoundError:
            try:
                self.schema = loadFromPackage('preset/%s.schema.yaml' % self.name, withNumbers=False)
            except FileNotFoundError:
                raise ValueError('您所指定的方案文件「%s.schema.yaml」不存在' % self.name)
        if 'aliaser' not in self.schema: self.schema['aliaser'] = {}
        self.parseSchema()
    
    def parseSchema(self):
        """
        功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
        输入：基础数据、用户方案（Schema）
        输出：用户字根索引字典 degeneracy 、键位索引字典 rootSet
        """
        # 检查笔画定义是否完整
        lostStrokes = checkCompleteness(self.schema['classifier'])
        if lostStrokes: # 若有缺失定义，发起错误
            raise ValueError('未定义的笔画：%s' % str(lostStrokes))
        for component in self.schema['aliaser']:
            indexList = self.schema['aliaser'][component][1]
            self.schema['aliaser'][component][1] = expand(indexList) # 展开省略式
        self.rootSet = {} # 字根名到键位的映射，用于取码时键位索引
        self.degeneracy = {} # 退化字根到字根的映射，用于构建powerDict
        allRoots = sum([list(x) for x in self.schema['mapper'].values()], [])
        self.diff_kou_wei = True if '口' in allRoots and '囗' in allRoots else False
        for key, rootList in self.schema['mapper'].items():
            for root in rootList:
                # 是单笔画字根
                if root in self.schema['classifier']:
                    for strokeType in self.schema['classifier'][root]:
                        self.rootSet[strokeType] = key
                        self.degeneracy[strokeType] = Char(strokeType, [Stroke([strokeType, None])])
                # 字根是「文」数据中的一个部件
                elif root in self.wen:
                    strokeList = [Stroke(stroke)
                                  for stroke in self.wen[root]]
                    objectChar = Char(root, strokeList)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    # self.degeneracy[characteristicString] = objectChar.name
                    # 本来以为只需要放一个名义字，但取末笔的时候要用到，故改为对象字
                    # 给这对字根添加额外的区分：
                    if root in '口囗' and self.diff_kou_wei:
                        self.kou_wei_cs = characteristicString
                        characteristicString += root
                    self.degeneracy[characteristicString] = objectChar
                # 字根不是「文」数据库中的部件，但用户定义了它
                elif root in self.schema['aliaser']:
                    source, indexer = self.schema['aliaser'][root]
                    l = len(self.wen[source])
                    sliceNum = sum(1 << (l - int(index) - 1) for n, index in enumerate(indexer))
                    strokeList = [Stroke(self.wen[source][int(index)])
                                  for index in indexer]
                    objectChar = Char(root, strokeList, sourceName=source, sourceSlice=sliceNum)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar
                # 这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
                elif root in self.zi:
                    self.complexRootList.append(root)
                    self.rootSet[root] = key
                else:
                    self.rootSet[root] = key

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
            characteristicString = self.degenerator(Char('', sliceStrokeList, objectChar.name, k))
            # 找不到退化字根的切片将会标记为None
            if self.diff_kou_wei and characteristicString == self.kou_wei_cs:
                if (k % 7 or objectChar.name in ['囗', '囱框']):
                    characteristicString += '囗'
                else:
                    characteristicString += '口'
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
            # bestEval = min(sieve(objectChar, scheme) for scheme in objectChar.schemeList)
            # selectBoolean = lambda scheme: sieve(objectChar, scheme) == bestEval
            # objectChar.schemeList = list(filter(selectBoolean, objectChar.schemeList))
            evalList = [sieve(objectChar, scheme) for scheme in objectChar.schemeList]
            bestEval = min(evalList)
            objectChar.schemeList = [x[0] for x in zip(objectChar.schemeList, evalList) if x[1] == bestEval]
        # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
        if len(objectChar.schemeList) == 1:
            # 理论上把字根的二进制表示放进去才完备，但除了 C 输入要用到之外都不用，先不写
            # return tuple(
            #     {
            #     'name': objectChar.powerDict[x], 
            #     'slice': x
            #     }
            #     for x in objectChar.schemeList[0])
            return tuple(objectChar.powerDict[x] for x in objectChar.schemeList[0])
        else:
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' % (objectChar.name, objectChar.schemeList))

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
        self.category = {}
        for category, strokeTypeList in self.schema['classifier'].items():
            for strokeType in strokeTypeList:
                self.category[strokeType] = category
        for complexRoot in self.complexRootList:
            componentList = self.tree[complexRoot].flatten()
            strokeList = sum([[Stroke(stroke) for stroke in self.wen[nameChar]] for nameChar in componentList], [])
            objectChar = Char(complexRoot, strokeList)
            self.component[complexRoot] = (objectChar, )
        for nameChar in self.wen:
            strokeList = [Stroke(stroke) for stroke in self.wen[nameChar]]
            objectChar = Char(nameChar, strokeList)
            objectChar.bestScheme = None
            # 某种捷径
            if nameChar in self.rootSet: 
                objectChar.bestScheme = (objectChar, )
                self.component[nameChar] = objectChar.bestScheme
                continue
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
    
    def output(self, directory=''):
        with open('%s%s.dict.yaml' % (directory, self.name), 'w', encoding='utf-8') as f: # 写进文件
            f.write('# Chai dictionary: %s\n\n---\nname: %s\n' % (self.name, self.name))
            if self.schema['schema'].get('version'):
                f.write('version: %s\n' % self.schema['schema'].get('version'))
            f.write('columns:\n  - text\n  - code\n...\n')
            for nameChar in self.charList:
                f.write('%s\t%s\n' % (nameChar, self.encoder[nameChar]))

class Erbi(Schema):

    def genRoot(self, objectChar):
        """
        功能：二笔的 powerDict 只含顺序取笔
        """
        for k in range(2, objectChar.charlen + 1):
            characteristicString = self.degenerator(Char('', objectChar.strokeList[:k], sourceName=objectChar.name, sourceSlice=((1 << k)-1)))
            if self.degeneracy.get(characteristicString):
                objectChar.root = self.degeneracy.get(characteristicString)
    
    def run(self):
        self.category = {}
        for category, strokeTypeList in self.schema['classifier'].items():
            for strokeType in strokeTypeList:
                self.category[strokeType] = category
        self.component = {}
        for nameChar in self.wen:
            strokeList = [Stroke(stroke) for stroke in self.wen[nameChar]]
            objectChar = Char(nameChar, strokeList)
            objectChar.root = None
            strokeCategoryList = [self.category[stroke.type] for stroke in strokeList]
            self.genRoot(objectChar)
            if objectChar.root:
                self.component[nameChar] = (objectChar.root.name, strokeCategoryList)
            else:
                self.component[nameChar] = (''.join(strokeCategoryList[:2]), strokeCategoryList)

    def parseSchema(self):
        """
        功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
        输入：基础数据、用户方案（Schema）
        输出：用户字根索引字典 degeneracy 、键位索引字典 rootSet
        """
        # 检查笔画定义是否完整
        lostStrokes = checkCompleteness(self.schema['classifier'])
        if lostStrokes: # 若有缺失定义，发起错误
            raise ValueError('未定义的笔画：%s' % str(lostStrokes))
        for component in self.schema['aliaser']:
            indexList = self.schema['aliaser'][component][1]
            self.schema['aliaser'][component][1] = expand(indexList) # 展开省略式
        self.rootSet = {} # 字根名到键位的映射，用于取码时键位索引
        self.degeneracy = {} # 退化字根到字根的映射，用于构建powerDict
        for key, rootList in self.schema['mapper'].items():
            for root in rootList:
                if root in self.schema['classifier']:
                    # 是单笔画字根
                    self.rootSet[root] = key
                elif len(root) == 2 and root[0] in self.schema['classifier'] and root[1] in self.schema['classifier']:
                    # 是双笔画字根
                    self.rootSet[root] = key
                # 字根是「文」数据中的一个部件
                elif root in self.wen:
                    strokeList = [Stroke(stroke)
                                  for stroke in self.wen[root]]
                    objectChar = Char(root, strokeList)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar
                # 字根不是「文」数据库中的部件，但用户定义了它
                elif root in self.schema['aliaser']:
                    source, indexer = self.schema['aliaser'][root]
                    l = len(self.wen[source])
                    sliceNum = sum(1 << (l - n - 1) for n, index in enumerate(indexer))
                    strokeList = [Stroke(self.wen[source][int(index)])
                                  for index in indexer]
                    objectChar = Char(root, strokeList, sourceName=source, sourceSlice=sliceNum)
                    self.rootSet[root] = key
                    characteristicString = self.degenerator(objectChar)
                    self.degeneracy[characteristicString] = objectChar
                # 这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
                elif root in self.zi:
                    pass