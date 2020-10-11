from pychai.base.character import Component
from pychai import Sequential, Character

def printDict(d):
    for key, value in d.items():
        if value:
            name = value.name
            print('%8s --- %s' % (bin(key)[2:],name))

class Wubi98(Sequential):
    '''
    叶类
    '''
    def oldPowerDict(self, component: Component):
        powerDict = {}
        # 生成掩码，二进制分别为 1，10，100……
        l = len(component.strokeList)
        mask = [1 << (l-i-1) for i in range(l)]
        for k in range(1, 2**l):
            # 数 k 与某个掩码按位与后，如果不为 0，那么说明k的二进制在掩码位为 1
            # 此时添加这一位对应的笔画
            indexList = []
            for index, item in enumerate(mask):
                if k & item:
                    indexList.append(index)
            fragment = component.fragment('', indexList)
            image = self.degenerator(fragment)
            # 找不到退化字根的切片将会标记为None
            powerDict[k] = self.degeneracy.get(image)
        return powerDict

    def new(self, component: Component):
        powerDict = {}
        for root in self.rootList:
            sliceBinaryCodeList = Sequential.findSliceV1(component, root)
            for sliceBinaryCode in sliceBinaryCodeList:
                powerDict[sliceBinaryCode] = root
        return powerDict

    def debug(self):
        for component in self.COMPONENTS.values():
            if component.name not in self.rootMap:
                p1 = self.oldPowerDict(component)
                p2 = self.new(component)
                for k, root in p2.items():
                    if p1[k] != root:
                        print(component.name)
                        printDict(p1)
                        print()
                        printDict(p2)

# 实例化拆分对象
wubi98 = Wubi98('templates/wubi98/wubi98.config.yaml')
wubi98.degeneracy = {}
for root in wubi98.rootList:
    image = wubi98.degenerator(root)
    wubi98.degeneracy[image] = root
wubi98.debug()

