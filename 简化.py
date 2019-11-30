import yaml

WEN = yaml.load(open('文.yaml', encoding='utf-8', mode='r'), Loader=yaml.BaseLoader)

# 预处理

class Point:
    """
    定义一个简单的二维向量类
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.c = (x, y)
        self.r = (x**2+y**2)**0.5

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __rmul__(self, scalar):
        x = scalar * self.x
        y = scalar * self.y
        return Point(x, y)

origin = Point(0, 0)

def chazhi(P0, Pc, P2):
    w1 = (1/(P0 - Pc).r)*(P0 - Pc)
    w2 = (1/(P2 - Pc).r)*(P2 - Pc)
    l = ((P0 - Pc).r * (P2 - Pc).r)**0.5
    P1 = Pc - 0.5 * l * (w1 + w2)
    return P1

def process(strokeType, argList):
    d10 = argList[1] - argList[0]
    bezierList = []
    if len(argList) == 2:
        if strokeType == '横':
            bezierList.append('h%d' % d10.x)
        elif strokeType == '竖':
            bezierList.append('v%d' % d10.y)
        elif strokeType == '提':
            bezierList.append('l%d %d' % d10.c)
        else:
            raise ValueError('不合法的笔画')
    elif len(argList) == 3:
        d20 = argList[2] - argList[0]
        d21 = argList[2] - argList[1]
        w012 = chazhi(origin, d10, d20)
        if strokeType == '提':
            bezierList.append('l%d %d' % d21.c)
        elif strokeType in '撇捺点':
            bezierList.append('q%d %d %d %d' % (w012.c + d20.c))
        elif strokeType == '横折':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d21.y)
        elif strokeType == '竖折':
            bezierList.append('v%d' % d10.y)
            bezierList.append('h%d' % d21.x)
        elif strokeType == '横钩':
            bezierList.append('h%d' % d10.x)
            bezierList.append('l%d %d' % d21.c)
        elif strokeType == '竖提':
            bezierList.append('v%d' % d10.y)
            bezierList.append('l%d %d' % d21.c)
    elif len(argList) == 4:
        d20 = argList[2] - argList[0]
        d21 = argList[2] - argList[1]
        d30 = argList[3] - argList[0]
        d31 = argList[3] - argList[1]
        d32 = argList[3] - argList[2]
        w012 = chazhi(origin, d10, d20)
        w013 = chazhi(origin, d10, d30)
        w123 = chazhi(origin, d21, d31)
        if strokeType == '撇':
            bezierList.append('q%d %d %d %d' % (w013.c + d30.c))
        elif strokeType == '横撇':
            bezierList.append('h%d' % d10.x)
            bezierList.append('q%d %d %d %d' % (w123.c + d31.c))
        elif strokeType == '横折折':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d21.y)
            bezierList.append('h%d' % d32.x)
        elif strokeType == '横折提':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d21.y)
            bezierList.append('l%d %d' % d32.c)
        elif strokeType == '竖钩':
            # 取最下面的点作为长度
            bezierList.append('v%d' % d20.y)
            # 然后取最下面的点到终点作为「钩」
            bezierList.append('l%d %d' % d32.c)
        elif strokeType == '竖弯':
            bezierList.append('v%d' % d10.y)
            bezierList.append('h%d' % d31.x)
        elif strokeType == '竖折折':
            bezierList.append('v%d' % d10.y)
            bezierList.append('h%d' % d21.x)
            bezierList.append('v%d' % d32.y)
        elif strokeType == '竖折撇':
            bezierList.append('l%d %d' % d10.c)
            bezierList.append('h%d' % d21.x)
            bezierList.append('q%d %d %d %d' % ((0.5*d32).c + d32.c))
        elif strokeType == '斜钩':
            bezierList.append('q%d %d %d %d' % (w012.c + d20.c))
            bezierList.append('l%d %d' % d32.c)
    elif len(argList) == 5:
        d20 = argList[2] - argList[0]
        d21 = argList[2] - argList[1]
        d30 = argList[3] - argList[0]
        d31 = argList[3] - argList[1]
        d32 = argList[3] - argList[2]
        d40 = argList[4] - argList[0]
        d41 = argList[4] - argList[1]
        d42 = argList[4] - argList[2]
        d43 = argList[4] - argList[3]
        w012 = chazhi(origin, d10, d20)
        w013 = chazhi(origin, d10, d30)
        w123 = chazhi(origin, d21, d31)
        w234 = chazhi(origin, d32, d42)
        if strokeType == '横折钩':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d31.y)
            bezierList.append('l%d %d' % d43.c)
        if strokeType == '横斜钩':
            bezierList.append('h%d' % d10.x)
            bezierList.append('q%d %d %d %d' % (w123.c + d31.c))
            bezierList.append('l%d %d' % d43.c)
        if strokeType == '横折折折':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d21.y)
            bezierList.append('h%d' % d32.x)
            bezierList.append('v%d' % d43.y)
        elif strokeType == '竖弯钩':
            bezierList.append('v%d' % d10.y)
            bezierList.append('h%d' % d31.x)
            bezierList.append('l%d %d' % d43.c)
        elif strokeType == '撇折':
            bezierList.append('q%d %d %d %d' % (w012.c + d20.c))
            bezierList.append('h%d' % d42.x)
        elif strokeType == '撇点':
            bezierList.append('q%d %d %d %d' % (w012.c + d20.c))
            bezierList.append('q%d %d %d %d' % (w234.c + d42.c))
        elif strokeType == '弯钩':
            bezierList.append('q%d %d %d %d' % (w013.c + d30.c))
            bezierList.append('l%d %d' % d43.c)
    elif len(argList) == 6:
        d20 = argList[2] - argList[0]
        d21 = argList[2] - argList[1]
        d30 = argList[3] - argList[0]
        d31 = argList[3] - argList[1]
        d32 = argList[3] - argList[2]
        d40 = argList[4] - argList[0]
        d41 = argList[4] - argList[1]
        d42 = argList[4] - argList[2]
        d43 = argList[4] - argList[3]
        d50 = argList[5] - argList[0]
        d51 = argList[5] - argList[1]
        d52 = argList[5] - argList[2]
        d53 = argList[5] - argList[3]
        d54 = argList[5] - argList[4]
        w012 = chazhi(origin, d10, d20)
        w013 = chazhi(origin, d10, d30)
        w123 = chazhi(origin, d21, d31)
        w234 = chazhi(origin, d32, d42)
        w345 = chazhi(origin, d43, d53)
        if strokeType == '横折折撇':
            bezierList.append('h%d' % d10.x)
            bezierList.append('l%d %d' % d21.c)
            bezierList.append('h%d' % d32.x)
            bezierList.append('q%d %d %d %d' % (w345.c + d53.c))
        elif strokeType == '横折弯钩':
            bezierList.append('h%d' % d10.x)
            bezierList.append('v%d' % d21.y)
            bezierList.append('h%d' % d42.x)
            bezierList.append('l%d %d' % d54.c)
        elif strokeType == '横撇弯钩':
            # 实际上是另一种「横折弯钩」
            bezierList.append('h%d' % d10.x)
            bezierList.append('l%d %d' % d21.c)
            bezierList.append('q%d %d %d %d' % (w234.c + d42.c))
            bezierList.append('l%d %d' % d54.c)
        elif strokeType == '竖折折钩':
            bezierList.append('v%d' % d10.y)
            bezierList.append('h%d' % d21.x)
            bezierList.append('v%d' % d42.y)
            bezierList.append('l%d %d' % d54.c)
    elif len(argList) == 7:
        d20 = argList[2] - argList[0]
        d21 = argList[2] - argList[1]
        d30 = argList[3] - argList[0]
        d31 = argList[3] - argList[1]
        d32 = argList[3] - argList[2]
        d40 = argList[4] - argList[0]
        d41 = argList[4] - argList[1]
        d42 = argList[4] - argList[2]
        d43 = argList[4] - argList[3]
        d50 = argList[5] - argList[0]
        d51 = argList[5] - argList[1]
        d52 = argList[5] - argList[2]
        d53 = argList[5] - argList[3]
        d54 = argList[5] - argList[4]
        d65 = argList[6] - argList[5]
        if strokeType == '横折折折钩':
            bezierList.append('h%d' % d10.x)
            bezierList.append('l%d %d' % d21.c)
            bezierList.append('h%d' % d32.x)
            bezierList.append('v%d' % d53.y)
            bezierList.append('l%d %d' % d65.c)
    return bezierList

CN = {}

with open('文.new.yaml', 'w') as f:
    for wen, strokeList in WEN.items():
        newStrokeList = []
        for stroke in strokeList:
            strokeType = stroke[0]
            argList = [Point(int(x[0]), int(x[1])) for x in stroke[1:]]
            bezier = ';'.join(process(strokeType, argList))
            result = '%s;m%d %d;%s' % (strokeType, argList[0].x, argList[0].y, bezier)
            newStrokeList.append(result)
        f.write('%s:\n' % wen)
        for stroke in newStrokeList:
            f.write('  - %s\n' % stroke)

        # strokeCN = len(stroke) - 1
        # if strokeType in CN:
        #     CN[strokeType].append(strokeCN)
        # else:
        #     CN[strokeType] = [strokeCN]

# CN = {key: list(set(value)) for key, value in CN.items()}
# CN_ = {}
# for key, value in CN.items():
#     for n in value:
#         if n not in CN_:
#             CN_[n] = [key]
#         else:
#             CN_[n].append(key)
