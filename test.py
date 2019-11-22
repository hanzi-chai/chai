def getPowerList(x):
    """
    输入：一个数
    输出：在保证第一部分取到数的二进制最高位的情况下，将它分为两个数之和，且求和时不进位
    """
    # l = [0]
    # while n:
    #     m = n - (n & (n-1))
    #     n = n & (n-1)
    #     l = l + [x + m for x in l]
    # return l
    x2 = x
    x3 = x
    while x2>0:
        x2 -= 1
        if x2&x == x3: continue
        yield x2&x
        x3 = x2

generator = getPowerList(12)
# print(getPowerList(12))
for i in generator:
    print(i)