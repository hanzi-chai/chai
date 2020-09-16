import math
import yaml
import pkgutil
from objects import Stroke, Char

TOL = 0.1

def inner(t):
    return (TOL < t) and (t < (1 - TOL))

def outer(t):
    return (-TOL < t) and (t < (1 + TOL))

def topo(t1, t2):
    if inner(t1) and inner(t2):
        return '交'
    elif outer(t1) and outer(t2):
        # 均为「连」类，要进一步细分；
        c1 = '前' if t1 < TOL else '中' if t1 < 1 - TOL else '后'
        c2 = '前' if t2 < TOL else '中' if t2 < 1 - TOL else '后'
        return c1 + c2 + '连'
    else:
        return '散'

def quadSolve(a, b, c):
    if abs(a) < 10**-10:
        x = -c / b
        if outer(x):
            return x
        else:
            return None
    delta = b*b - 4*a*c
    if delta > 0:
        s = math.sqrt(delta)
        x1 = (-b + s)/2/a
        x2 = (-b - s)/2/a
        if outer(x1) and outer(x2):
            raise ValueError('实际上应该没有这个情况')
        elif outer(x1):
            return x1
        elif outer(x2):
            return x2
        else:
            return None
    elif delta < 0:
        return None
    else:
        raise ValueError('没这么巧吧？')

def bisection(f, xmin, xmax, epsilon):
    if f(xmin) * f(xmax) > 0:
        return None
    else:
        left = xmin
        right = xmax
        while (right - left > epsilon):
            middle = (left + right)/2
            if f(middle) * f(right) > 0:
                right = middle
            else:
                left = middle
        return (left + right)/2

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, another):
        return Point(self.x + another.x, self.y + another.y)
    
    def __sub__(self, another):
        return Point(self.x - another.x, self.y - another.y)

    def __mul__(self, another):
        return self.x * another.y - self.y * another.x
    
    def __rmul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y)
    
    def solve(self, p1, p2):
        det = p1 * p2
        if det != 0:
            t1 = (self * p2) / det
            t2 = (p1 * self) / (p1 * p2)
            return (t1, t2)
        else:
            return (None, None)
    
    def __str__(self):
        return '(%d, %d)' % (self.x, self.y)

class Bezier():
    pass

class Linear(Bezier):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __and__(self, another):
        if isinstance(another, Quadratic):
            return another & self
        else:
            p1 = self.end - self.start
            p2 = another.start - another.end
            b = another.start - self.start
            t1, t2 = b.solve(p1, p2)
            if t1 != None:
                return topo(t1, t2)
            else:
                return '散'
    
    def __str__(self):
        return 'Linear Bezier Curve: %s -> %s' % (self.start, self.end)

class Quadratic(Bezier):
    def __init__(self, start, mid, end):
        self.start = start
        self.mid = mid
        self.end = end
    
    def __and__(self, another):
        if isinstance(another, Linear):
            l1 = another.end - another.start
            l0 = another.start
            r2 = self.start + self.end - (2 * self.mid)
            r1 = 2 * (self.mid - self.start)
            r0 = self.start
            # 此处可能出现数值不稳定，采用列主元消元法
            if abs(l1.x) > abs(l1.y):
                multiplier = l1.y / l1.x
                a = r2.y - multiplier * r2.x
                b = r1.y - multiplier * r1.x
                c = (r0.y - multiplier * r0.x) - (l0.y - multiplier * l0.x)
                t3 = quadSolve(a, b, c)
                if t3 != None:
                    t1 = ((t3**2)*r2.x + t3*r1.x + r0.x - l0.x) / l1.x
                    return topo(t1, t3)
                else:
                    return '散'
            else:
                multiplier = l1.x / l1.y
                a = r2.x - multiplier * r2.y
                b = r1.x - multiplier * r1.y
                c = (r0.x - multiplier * r0.y) - (l0.x - multiplier * l0.y)
                t3 = quadSolve(a, b, c)
                if t3 != None:
                    t1 = ((t3**2)*r2.y + t3*r1.y + r0.y - l0.y) / l1.y
                    return topo(t1, t3)
                else:
                    return '散'
        else:
            l2 = self.start + self.end - 2 * self.mid
            l1 = 2 * (self.mid - self.start)
            l0 = self.start
            r2 = another.start + another.end - 2 * another.mid
            r1 = 2 * (another.mid - another.start)
            r0 = another.start
            if abs(l2.x) > abs(l2.y):
                multiplier = l2.y / l2.x
                nl1 = l1.y - multiplier * l1.x
                nl0 = l0.y - multiplier * l0.x
                nr2 = r2.y - multiplier * r2.x
                nr1 = r1.y - multiplier * r1.x
                nr0 = r0.y - multiplier * r0.x
                e2 = nr2 / nl1
                e1 = nr1 / nl1
                e0 = (nr0 - nl0) / nl1
                s4 = l2.x * e2**2
                s3 = l2.x * 2*e2*e1
                s2 = l2.x * (e1**2 + 2*e2*e0) + l1.x * e2 - r2.x
                s1 = l2.x * 2*e1*e0 + l1.x * e1 - r1.x
                s0 = l2.x * e0**2 + l1.x * e0 + l0.x - r0.x
                def f(x): return s4 * x**4 + s3 * x**3 + s2 * x**2 + s1 * x + s0
                t4 = bisection(f, -TOL, 1 + TOL, 0.001)
                if t4 != None:
                    t3 = e2 * t4**2 + e1 * t4 + e0
                    return topo(t3, t4)
                else:
                    return '散'
            else:
                multiplier = l2.x / l2.y
                nl1 = l1.x - multiplier * l1.y
                nl0 = l0.x - multiplier * l0.y
                nr2 = r2.x - multiplier * r2.y
                nr1 = r1.x - multiplier * r1.y
                nr0 = r0.x - multiplier * r0.y
                e2 = nr2 / nl1
                e1 = nr1 / nl1
                e0 = (nr0 - nl0) / nl1
                s4 = l2.y * e2**2
                s3 = l2.y * 2*e2*e1
                s2 = l2.y * (e1**2 + 2*e2*e0) + l1.y * e2 - r2.y
                s1 = l2.y * 2*e1*e0 + l1.y * e1 - r1.y
                s0 = l2.y * e0**2 + l1.y * e0 + l0.y - r0.y
                def f(x): return s4 * x**4 + s3 * x**3 + s2 * x**2 + s1 * x + s0
                t4 = bisection(f, -TOL, 1 + TOL, 0.001)
                if t4 != None:
                    t3 = e2 * t4**2 + e1 * t4 + e0
                    return topo(t3, t4)
                else:
                    return '散'
    
    def __str__(self):
        return 'Quadratic Bezier Curve: %s -> %s -> %s' % (self.start, self.mid, self.end)

def topology(objectChar):
    strokeList = objectChar.strokeList
    strokeListAug = []
    for stroke in strokeList:
        bezierList = []
        previous = Point(*stroke.start[1:])
        for command in stroke.drawList:
            if len(command) <= 3:
                if command[0] == 'h': now = previous + Point(command[1], 0)
                elif command[0] == 'v': now = previous + Point(0, command[1])
                else: now = previous + Point(*command[1:])
                bezierList.append(Linear(previous, now))
            else:
                passby = previous + Point(*command[1:3])
                now = previous + Point(*command[3:])
                bezierList.append(Quadratic(previous, passby, now))
            previous = now
        strokeListAug.append(bezierList)
    returnList = []
    for n, bezierList in enumerate(strokeListAug):
        row = []
        for n_, bezierList_ in enumerate(strokeListAug):
            if n_ >= n: continue
            relationList = []
            for bezier in bezierList:
                for bezier_ in bezierList_:
                    relationList.append(bezier & bezier_)
            row.append('_'.join(relationList))
        returnList.append(row)
    return returnList
    # return ' '.join(' '.join(x & y for i, x in enumerate(bezierList) if i < j) for j, y in enumerate(bezierList))

if __name__ == "__main__":
    """
    这里是生成字典备查用的代码，但现在是放到 degenerator 中调用，所以用不到
    """
    WEN = yaml.load(open('Chai/文.yaml'), Loader=yaml.SafeLoader)
    # WEN = yaml.load(open('Chai/文.test.yaml'), Loader=yaml.SafeLoader)
    TOPO = {nameChar: topology(Char(nameChar, [Stroke(stroke) for stroke in strokeList])) for nameChar, strokeList in WEN.items()}

    with open('Chai/文.topo.yaml', encoding='utf-8', mode='w') as f:
    # with open('文.topo.test.yaml', encoding='utf-8', mode='w') as f:
        for nameChar, topoString in TOPO.items():
            f.write('%s: %s\n' % (nameChar, topoString))
