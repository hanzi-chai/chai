import yaml

class Stroke:
    """
    定义一个笔画对象，包括类别（横竖撇点折）和起点、终点、经过点。
    横竖一般不写经过点，撇点一般要写经过点以描述弯曲。
    """
    def __init__(self, object):
        self.type = object['type']
        self.start = object['start']
        self.end = object['end']
    
    def __str__(self):
        return str(self.type) + ':' + str(self.start) + '->' + str(self.end) + ' '

class Char:
    """
    根据笔画来创建一个字
    """
    def __init__(self, name, strokeList):
        self.name = name
        self.strokeList = strokeList
    
    def getLen(self):
        """
        返回字的笔画数
        """
        return len(self.strokeList)
    
    def getOrder(self):
        """
        返回字的笔顺
        """
        return [stroke.category for stroke in self.strokeList]

    def identity(self, another):
        """
        输入：两个字
        输出：判断这两个字是不是相等；这里用了一个非常粗略的判据，即只判定笔顺
        """
        return self.getOrder() == another.getOrder()

    def allPossibleScheme(self, roots):
        """
        输入：字和字根集
        输出：在给定字根集下，所有可能的拆分
        """
        schemes = {(self, ): '未拆完'}
        # 将拆分列表进行迭代，每次选取未拆完的一个对象，将最后一个组件拆分一次
        while True:
            newSchemes = {}
            for i in schemes:
                cont = False
                if schemes[i] == '未拆完':
                    cont = True
                    residue = i[-1]
                    powerList = residue.getPowerList()
                    for newChar, newRes in powerList:
                        for root in roots:
                            if newChar.identity(root):
                                newChar.name = root.name
                                if newRes.strokeList:
                                    newSchemes[i[:-1] + (newChar, newRes)] = '未拆完' 
                                else:
                                    newSchemes[i[:-1] + (newChar, )] = '已拆完'
                                break
                else:
                    newSchemes[i] = schemes[i]
            if not cont: break
            schemes = newSchemes
        return schemes
    
    def getPowerList(self):
        """
        输入：字
        输出：把字分为两部分，第一部分含首笔，第二部分不含首笔，输出所有这样划分的可能性
        """
        n = self.getLen() - 1
        strokeList = self.strokeList
        marks = [ 1<<i for i in range(0, n) ]
        powerList = []
        for k in range(2**n):
            newCharList = [strokeList[0]]
            newResList = []
            for idx, item in enumerate(marks):
                if k & item:
                    newCharList.append(strokeList[idx + 1])
                else:
                    newResList.append(strokeList[idx + 1])
            newChar = Char('', newCharList)
            newRes = Char('', newResList)
            powerList.append((newChar, newRes))
        return powerList
    
    def __str__(self):
        return self.name + '{\n\t' + '\n\t'.join(str(stroke) for stroke in self.strokeList) + '\n\t}'

def evaluate(scheme):
    """
    输入：一个拆分
    输出：对拆分的估值，估值越大越优先，这里采用的规则是「取大优先」
    """
    n = 0
    for index, char in enumerate(scheme):
        n += 10**(-index) * char.getLen()
    return n

zi = yaml.load_all(open('Zi.yaml'), Loader=yaml.BaseLoader)
CHARLIST = []
for i in zi:
    print(i)

# 「木」的四个笔画
heng = Stroke('横', (0.1, 0.2), (0.9, 0.2))
shu = Stroke('竖', (0.5, 0.1), (0.5, 0.9))
pie = Stroke('撇', (0.5, 0.2), (0.05, 0.8), (0.3, 0.6))
dian = Stroke('点', (0.5, 0.2), (0.95, 0.8), (0.7, 0.6))

# 初始化「木」，并同时初始化一个字根「十」
mu = Char('木', (heng, shu, pie, dian))
shi = Char('十', (heng, shu))
zigenheng = Char('一', (heng, ))
zigenshu = Char('丨', (shu, ))
zigenpie = Char('丿', (pie, ))
zigendian = Char('丶', (dian, ))

# # 将「十」选作字根，当然单笔画也是字根
# roots = {shi, zigenheng, zigenshu, zigenpie, zigendian}

# # 生成「木」的所有拆分可能性。应该有两种：拆成「十+3+4」和拆成「1+2+3+4」
# schemes = mu.allPossibleScheme(roots)
# # 对拆分进行估值，第一种给出 2.11，第二种给出 1.111，所以第一种胜出
# schemesEvaluate = [(scheme, evaluate(scheme)) for scheme in schemes]
# schemesEvaluate = sorted(schemesEvaluate, key=lambda x: x[1], reverse=True)
# bestScheme = schemesEvaluate[0][0]
# bestScore = schemesEvaluate[0][1]
# print('汉字「%s」的拆分结果为：' % mu.name)
# for index, char in enumerate(bestScheme):
#     print('第 %d 个字根是：' % (index + 1), char)
