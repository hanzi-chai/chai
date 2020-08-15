from typing import Dict
from pychai.data import *
from pychai.preset_fn import *
from pychai.types import *
import time

# TODO: 分离出与erbi.py共同的通用框架
class Chai:
    """
    方案拆分类：
        - 解析函数
    """
    tree = {}
    complexRootList = []
    encoder = {}
    # 预设的退化映射组件
    __fieldDict = {
        '笔画序列': getStrokeList,
        '笔画序列（简）': getStrokeListSimplified,
        '笔画拓扑': getTopoList
    }
    # 预设的择优函数
    __sieveDict = {
        '根少优先': schemeLen,
        '笔顺优先': schemeOrder,
        '能连不交、能散不连': schemeTopo,
        '取大优先': schemeBias
    }
    def __init__(self, schemaName: str):
        """
        功能：加载基础数据，并加载用户方案（暂定）
        """
        self.name = schemaName # 设置方案名，下面import时schema.py会读取使用
        for nameChar, expression in ZI.items():
            tree = Tree(nameChar, expression, ZI)
            self.tree[nameChar] = tree
        allKeys = list(WEN.keys()) + list(ZI.keys())
        self.charList = sorted(filter(lambda x: len(x) == 1, allKeys), key = ord)

    def setField(self, fieldName, field):
        """
        功能：供用户设置自定义的退化映射组件
        """
        self.__fieldDict[fieldName] = field

    def setSieve(self, sieveName, sieve):
        """
        功能：供用户设置自定义的择优函数
        """
        self.__sieveDict[sieveName] = sieve

    def genPowerDict(self, objectChar: Char):
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
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明k的二进制在掩码位为 1
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

    # def genBestScheme(self, objectChar):
    #     objectChar.bestScheme = self.selector(objectChar)

    # def degenerator(self, objectChar):
    #     characteristicString = ''
    #     if objectChar.charlen > 1:
    #         for fieldName in DEGENERATOR:
    #             field = self.__fieldDict[fieldName]
    #             characteristicString += field(objectChar)
    #     else:
    #         characteristicString = objectChar.strokeList[0].type
    #     return characteristicString

    # def selector(self, objectChar):
    #     for sieveName in SELECTOR:
    #         sieve = self.__sieveDict[sieveName]
    #         # bestEval = min(sieve(objectChar, scheme) for scheme in objectChar.schemeList)
    #         # selectBoolean = lambda scheme: sieve(objectChar, scheme) == bestEval
    #         # objectChar.schemeList = list(filter(selectBoolean, objectChar.schemeList))
    #         evalList = [sieve(objectChar, scheme) for scheme in objectChar.schemeList]
    #         bestEval = min(evalList)
    #         objectChar.schemeList = [x[0] for x in zip(objectChar.schemeList, evalList) if x[1] == bestEval]
    #     # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
    #     if len(objectChar.schemeList) == 1:
    #         # 理论上把字根的二进制表示放进去才完备，但除了 C 输入要用到之外都不用，先不写
    #         # return tuple(
    #         #     {
    #         #         'name': objectChar.powerDict[x],
    #         #         'slice': x
    #         #     }
    #         #     for x in objectChar.schemeList[0])
    #         return tuple(objectChar.powerDict[x] for x in objectChar.schemeList[0])
    #     else:
    #         raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' % (objectChar.name, objectChar.schemeList))

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
            strokeList = sum([[Stroke(stroke) for stroke in WEN[nameChar]] for nameChar in componentList], [])
            objectChar = Char(complexRoot, strokeList)
            self.component[complexRoot] = (objectChar, )
        for nameChar in WEN:
            strokeList = [Stroke(stroke) for stroke in WEN[nameChar]]
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

    def nextRoot(self,n):
        """
        功能：给定字未拆完的部分，求拆出下一个字根的所有可能性
        输入：数 n
        输出：在数的二进制表示中左边第一位取 1 ，其余所有「1」的位上取 1 或取 0
            的所有可能的数的列表
        备注：一个含有n笔的字可用一个十进制数2**n-1表达其笔画状态
            例如一个3笔的字可以用7来表示，其对应二进值是111
            对于字的任意切片，可同理表示，上字含首末笔的切片为101，对应十进值为5
            以下算法基于位运算
        """
        powerList = [0]
        while n: # 直到当前序列所有「1」位都被置0之前，做：
            # 找到右边第一个「1」，如1110010的右二位，将其置0，得余待检序列1110000
            t = n & (n-1)
            # 当前序列扣除余待检序列，获得当前位及其右边所有位，1110010-1110000=10
            m = n - t
            # 将余待检序列设为当前序列，用于下一loop
            n = t
            # 对列表中每一个已有位扩增当前位「1」，并以此列表扩增原列表
            powerList = powerList + [x + m for x in powerList]
            # 当前位的「0」选项，将会在下一位「1」扩增时扩增
        # 将所有不足笔数长度的序列剔除，表明所取切片必含输入切片的第一笔
        return powerList[len(powerList)//2:]