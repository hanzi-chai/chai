'''
经典形码
'''

from collections import deque
from typing import List
from .chai import Chai
from ..base import Component, Compound, Fragment

class Sequential(Chai):
    '''
    经典形码
    '''

    def __addPowerDict(self, component: Component) -> None:
        '''
        功能：解析出基础字的所有有效切片，构造切片到用户字根的字典 powerDict
        输入：基础字的对象字
        输出：将 powerDict 传给对象字
        备注1：有效切片是由用户定义的字根定义的
        备注2：依赖退化函数 degenerate ，依赖用户字根索引字典 degeneracy
        '''
        component.powerDict = {}
        # 生成掩码，二进制分别为 1，10，100……
        l = len(component.strokeList)
        mask = [1 << (l-i-1) for i in range(l)]
        for k in range(1, 2**l):
            sliceStrokeList = []
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明k的二进制在掩码位为 1
            # 此时添加这一位对应的笔画
            indexList = []
            for index, item in enumerate(mask):
                if k & item:
                    sliceStrokeList.append(component.strokeList[index])
                    indexList.append(index)
            fragment = Fragment('', sliceStrokeList, component, indexList)
            image = self.degenerator(fragment)
            # 找不到退化字根的切片将会标记为None
            component.powerDict[k] = self.degeneracy.get(image)

    def __addSchemeList(self, component: Component) -> None:
        '''
        功能：解析出在给定字根集下对象字的所有有效的拆分
        输入：对象字（字、字根）
        输出：将所有有效的拆分 schemeList 传给 objectChar
        '''
        l = len(component.strokeList)
        # 建立一个字典记录拆分状态，若已拆完则为真，否则为假
        queue = deque([(2**l - 1, )])
        schemeList = []
        # 将拆分列表进行迭代，每次选取未拆完的一个对象，将最后一个组件拆分一次
        while queue:
            scheme = queue.popleft()
            residue = scheme[-1]
            # 上一行：无效切片会因为返回None而被filter筛除
            rootList = list(filter(lambda x: component.powerDict[x], self.__nextRoot(residue)))
            for root in rootList:
                if root != residue: # 没拆完
                    queue.append(scheme[:-1] + (root, residue - root))
                else: # 新拆出的字根和原有剩余一样大，说明已拆完
                    schemeList.append(scheme)
        component.schemeList = schemeList

    @staticmethod
    def __nextRoot(n) -> List[int]:
        '''
        功能：给定字未拆完的部分，求拆出下一个字根的所有可能性
        输入：数 n
        输出：在数的二进制表示中左边第一位取 1 ，其余所有「1」的位上取 1 或取 0
            的所有可能的数的列表
        备注：一个含有n笔的字可用一个十进制数2**n-1表达其笔画状态
            例如一个3笔的字可以用7来表示，其对应二进值是111
            对于字的任意切片，可同理表示，上字含首末笔的切片为101，对应十进值为5
            以下算法基于位运算
        '''
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

    def _getComponentScheme(self, component: Component) -> None:
        if component.name in self.rootMap:
            component.scheme = (component,)
        else:
            self.__addPowerDict(component)
            self.__addSchemeList(component)
            self.selector(component)

    def _getCompoundScheme(self, compound: Compound) -> None:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        compound.scheme = firstChild.scheme + secondChild.scheme
