import turtle
import yaml

PF = {}
with open('../../../Public/存档/输入方案/苹方/苹方极细.txt') as f:
    for line in f:
        char, path = line.strip('\r\n').split('\t')
        path = [x.strip().split(' ') for x in path.split(';')]
        PF[char] = path

WEN = yaml.load(open('文.patch.yaml'), Loader=yaml.BaseLoader)

# 类 TTF 数据库格式
# for char, strokeList in ZI.items():
#     newStrokeList = []
#     for stroke in strokeList:
#         start, path = stroke.split(' ', 1)[1].split(';', 1)
#         start = [int(x) for x in start.split(' ')]
#         pathList = [x.split() for x in path.split(';')]
#         newStrokeList.append((start, pathList))
#     ZI[char] = newStrokeList

n = 5
ts = [1/n * i for i in range(1, n+1)]

turtle.setup(width=1000, height=1000)
turtle.setworldcoordinates(0, 1000, 1000, 0)
turtle.color('blue')
turtle.speed(0)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.c = (x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __rmul__(self, scalar):
        x = scalar * self.x
        y = scalar * self.y
        return Point(x, y)

def cubic(t, P1, P2, P3, P4):
    return (1-t)**3*P1 + 3*(1-t)**2*t*P2 + 3*(1-t)*t**2*P3 + t**3*P4

def pos():
    x, y = turtle.pos()
    return Point(x, y)

def move(dr):
    r = pos()
    r = r + dr
    turtle.goto(r.c)

def m(argList):
    turtle.pu()
    dr = Point(argList[0], argList[1])
    move(dr)
    # turtle.goto(dr.c)
    turtle.pd()

def h(argList):
    move(Point(argList[0], 0))

def v(argList):
    move(Point(0, argList[0]))

def l(argList):
    move(Point(argList[0], argList[1]))

def c(argList):
    x1, y1, x2, y2, x3, y3 = argList
    this = pos()
    first = this + Point(x1, y1)
    # 一类规则
    second = first + Point(x2, y2)
    end = second + Point(x3, y3)
    # 另一类规则
    # second = this + Point(x2, y2)
    # end = this + Point(x3, y3)
    for t in ts:
        r = cubic(t, this, first, second, end)
        turtle.goto(r.c)

target = '戍'
yi = PF[target]
print(yi)
for stroke in yi:
    print(stroke)
    func = stroke[0]
    argList = [float(x) for x in stroke[1:]]
    eval(func)(argList)

turtle.color('red')
turtle.pu()

zi = WEN[target]

# # 类 TTF
# for stroke in zi:
#     start, pathList = stroke
#     start = Point(start[0], start[1])
#     turtle.goto(start.c)
#     turtle.pd()
#     for path in pathList:
#         func = path[0]
#         argList = [int(x) for x in path[1:]]
#         eval(func)(argList)
#     turtle.pu()

# 文泉驿
for stroke in zi:
    points = stroke[1:]
    # print(points)
    turtle.goto(float(i) for i in points[0])
    turtle.pd()
    for point in points[1:]:
        turtle.goto(float(i) for i in point)
    turtle.pu()

turtle.exitonclick()
turtle.done()