class Point:
    """
    对象：一个简单的二维向量
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.c = (x, y)

    def __add__(self, another):
        x = self.x + another.x
        y = self.y + another.y
        return Point(x, y)

    def __rmul__(self, scalar):
        x = scalar * self.x
        y = scalar * self.y
        return Point(x, y)

class Line(Bezier):
    """
    对象：一次贝塞尔曲线，简称直线
    成员：起点，终点
    方法：
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

class Curve(Bezier):
    """
    对象：二次贝塞尔曲线，简称曲线
    成员：起点，终点
    方法：
    """

    def __init__(self, start, mid, end):
        self.start = start
        self.mid = mid
        self.end = end

def relation_ll(l1, l2):
    