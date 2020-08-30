from typing import List
from .chai_abstract import ChaiAbstract
from pychai.classes import Char, UnitChar, Stroke
import time

class ChaiClassical(ChaiAbstract):
    """
    方案拆分类：
        - 解析函数
    """
    def __init__(self, schemaName: str, path: str=''):
        """
        功能：加载基础数据，并加载用户方案（暂定）
        """
        super().__init__(schemaName, path)
        self.gpdTime = 0
        self.decTime = 0
        self.selTime = 0

    def __genPowerDict(self, unitChar: UnitChar) -> None:
        """
        功能：解析出基础字的所有有效切片，构造切片到用户字根的字典 powerDict
        输入：基础字的对象字
        输出：将 powerDict 传给对象字
        备注1：有效切片是由用户定义的字根定义的
        备注2：依赖退化函数 degenerate ，依赖用户字根索引字典 degeneracy
        """
        unitChar.powerDict = {}
        # 生成掩码，二进制分别为 1，10，100……
        l = len(unitChar.strokeList)
        mask = [1 << (l-i-1) for i in range(l)]
        for k in range(1, 2**l):
            sliceStrokeList = []
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明k的二进制在掩码位为 1
            # 此时添加这一位对应的笔画
            for idx, item in enumerate(mask):
                if k & item:
                    sliceStrokeList.append(unitChar.strokeList[idx])
            characteristicString = self.degenerator(
                UnitChar('', sliceStrokeList, unitChar.name, k))
            # 找不到退化字根的切片将会标记为None
            unitChar.powerDict[k] = self.degeneracy.get(characteristicString)

    def __genSchemeList(self, unitChar: UnitChar) -> None:
        """
        功能：解析出在给定字根集下对象字的所有有效的拆分
        输入：对象字（字、字根）
        输出：将所有有效的拆分 schemeList 传给 objectChar
        """
        l = len(unitChar.strokeList)
        # 建立一个字典记录拆分状态，若已拆完则为真，否则为假
        uncompletedList = [(2**l - 1, )]
        completedList = []
        # 将拆分列表进行迭代，每次选取未拆完的一个对象，将最后一个组件拆分一次
        while uncompletedList:
            newUncompletedList = []
            for scheme in uncompletedList:
                residue = scheme[-1]
                rootList = list(filter(lambda x: unitChar.powerDict[x], self.__nextRoot(residue)))
                # 上一行：无效切片会因为返回None而被filter筛除
                for root in rootList:
                    if root != residue: # 没拆完
                        newUncompletedList.append(scheme[:-1] + (root, residue - root))
                    else: # 新拆出的字根和原有剩余一样大，说明已拆完
                        completedList.append(scheme)
            uncompletedList = newUncompletedList
        unitChar.possibleSchemeList = completedList

    def __nextRoot(self, n) -> List[int]:
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
            t = n & (n - 1)
            # 当前序列扣除余待检序列，获得当前位及其右边所有位，1110010-1110000=10
            m = n - t
            # 将余待检序列设为当前序列，用于下一loop
            n = t
            # 对列表中每一个已有位扩增当前位「1」，并以此列表扩增原列表
            powerList = powerList + [x + m for x in powerList]
            # 当前位的「0」选项，将会在下一位「1」扩增时扩增
        # 将所有不足笔数长度的序列剔除，表明所取切片必含输入切片的第一笔
        return powerList[len(powerList)//2:]

    def genSchemeUnitChar(self, unitChar: UnitChar) -> None:
        if unitChar.name in self.rootKeymap:
            unitChar.scheme = [unitChar]
        else:
            time0 = time.perf_counter()
            self.__genPowerDict(unitChar)
            time1 = time.perf_counter()
            self.__genSchemeList(unitChar)
            time2 = time.perf_counter()
            self.selector(unitChar)
            time3 = time.perf_counter()
            self.gpdTime += time1 - time0
            self.decTime += time2 - time1
            self.selTime += time3 - time2

    def genScheme(self) -> None:
        super().genScheme()
        print("取幂集耗时：%.2f，拆分字根耗时：%.2f，择优耗时：%.2f" \
            % (self.gpdTime, self.decTime, self.selTime))

    # def run(self):
    #     """
    #     功能：解析出文数据库中字按拆分逻辑及用户定义字根拆分出的拆分列
    #          建立文数据库中字到拆分列的字典
    #     输入：基础数据、用户方案
    #     输出：基础字根拆分索引字典component
    #     """
    #     """
    #     嵌套拆分
    #     输入：字
    #     输出：计算一个字所依赖的所有其他字（文数据库中的基础字/部件）
    #     """
    #     self.component = {}
    #     gpdTime = 0
    #     decTime = 0
    #     selTime = 0
    #     self.category = {}
    #     # TODO:暂时不知道干嘛用的
    #     for category, strokeTypeList in self.schema['classifier'].items():
    #         for strokeType in strokeTypeList:
    #             self.category[strokeType] = category
    #     # 合成根
    #     for complexRoot in self.complexRootList:
    #         componentList = self.tree[complexRoot].flatten()
    #         strokeList = sum([[Stroke(stroke) for stroke in WEN[nameChar]] for nameChar in componentList], [])
    #         objectChar = Char(complexRoot, strokeList)
    #         self.component[complexRoot] = (objectChar, )
    #     # 拆分
    #     for nameChar in WEN:
    #         strokeList = [Stroke(stroke) for stroke in WEN[nameChar]]
    #         objectChar = Char(nameChar, strokeList)
    #         objectChar.bestScheme = None
    #         # 某种捷径
    #         if nameChar in self.rootSet:
    #             objectChar.bestScheme = (objectChar, )
    #             self.component[nameChar] = objectChar.bestScheme
    #             continue
    #         time0 = time.time()
    #         # 取幂集
    #         self.genPowerDict(objectChar)
    #         time1 = time.time()
    #         # 拆分
    #         self.genSchemeList(objectChar)
    #         time2 = time.time()
    #         # 择优
    #         self.genBestScheme(objectChar)
    #         time3 = time.time()
    #         # 将字到拆分列写入映射
    #         self.component[nameChar] = objectChar.bestScheme
    #         self.gpdTime += time1 - time0
    #         self.decTime += time2 - time1
    #         self.selTime += time3 - time2
