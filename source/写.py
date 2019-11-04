import turtle

with open('PingFang.txt', 'r') as f:
    charList = [line.strip('\r\n').split('\t') for line in f]

ts = [0.2 * i for i in range(1, 6)]

charDict = {}
for item in charList:
    char, unicode, path = item
    pathList = path.split('; ')
    newPathList = []
    for path in pathList:
        index = path.find('(')
        func = path[:index]
        argList = eval(path[index:])
        newPathList.append((func, argList))
    charDict[char] = newPathList

turtle.setup(width=1000, height=1000)
turtle.color('blue')
turtle.speed(10)
turtle.pu()
turtle.goto(-500, -300)
turtle.pd()

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

def hmove(arg):
    turtle.pu()
    dr = Point(arg, 0)
    move(dr)
    turtle.pd()

def vmove(arg):
    turtle.pu()
    dr = Point(0, arg)
    move(dr)
    turtle.pd()

def rmove(argList):
    turtle.pu()
    dr = Point(argList[0], argList[1])
    move(dr)
    turtle.pd()

def hline(argList):
    h = True
    if type(argList) == type(0):
        move(Point(argList, 0))
    else:
        for arg in argList:
            if h:
                move(Point(arg, 0))
            else:
                move(Point(0, arg))
            h = not h

def vline(argList):
    h = False
    if type(argList) == type(0):
        move(Point(0, argList))
    else:
        for arg in argList:
            if h:
                move(Point(arg, 0))
            else:
                move(Point(0, arg))
            h = not h

def rline(argList):
    for index in range(len(argList) // 2):
        move(Point(argList[index], argList[index + 1]))

def hhcurve(argList):
    x1, x2, y1, x3 = argList
    this = pos()
    first = this + Point(x1, 0)
    second = first + Point(x2, y1)
    end = second + Point(x3, 0)
    for t in ts:
        r = cubic(t, this, first, second, end)
        turtle.goto(r.c)

def hvcurve(argList):
    x1, y1, x2, y2 = argList
    this = pos()
    first = this + Point(x1, 0)
    second = first + Point(x2, y1)
    end = second + Point(0, y2)
    for t in ts:
        r = cubic(t, this, first, second, end)
        turtle.goto(r.c)

def vhcurve(argList):
    y1, x1, y2, x2 = argList
    this = pos()
    first = this + Point(0, y1)
    second = first + Point(x1, y2)
    end = second + Point(x2, 0)
    for t in ts:
        r = cubic(t, this, first, second, end)
        turtle.goto(r.c)

def vvcurve(argList):
    y1, y2, x1, y3 = argList
    this = pos()
    first = this + Point(0, y1)
    second = first + Point(x1, y2)
    end = second + Point(0, y3)
    for t in ts:
        r = cubic(t, this, first, second, end)
        turtle.goto(r.c)

def rrcurve(argList):
    p = len(argList) // 6
    for i in range(p):
        x1, y1, x2, y2, x3, y3 = argList[6*i:6*(i+1)]
        this = pos()
        first = this + Point(x1, y1)
        second = first + Point(x2, y2)
        end = second + Point(x3, y3)
        for t in ts:
            r = cubic(t, this, first, second, end)
            turtle.goto(r.c)

def rcurveline(argList):
    rrcurve(argList[:-2])
    rline(argList[-2:])

def rlinecurve(argList):
    rline(argList[:2])
    rrcurve(argList[2:])

yi = charDict['我']
for func, argList in yi:
    print(func, argList)
    eval(func)(argList)

# turtle.color('red')
# turtle.pu()
# turtle.goto(-430, 67)
# turtle.pd()
# turtle.goto(430, 67)
turtle.exitonclick()
turtle.done()