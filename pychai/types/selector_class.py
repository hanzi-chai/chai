class Selector():
    def __init__(self,sieves: List[Callable[[Char],None]]):
        self.sieves = sieves

    def __call__(self,objectChar: Char)->None:
        for sieve in self.sieves:
            # bestEval = min(sieve(objectChar, scheme) for scheme in objectChar.schemeList)
            # selectBoolean = lambda scheme: sieve(objectChar, scheme) == bestEval
            # objectChar.schemeList = list(filter(selectBoolean, objectChar.schemeList))
            evalList = [sieve(objectChar, scheme) for scheme in objectChar.schemeList]
            bestEval = min(evalList)
            objectChar.schemeList = [x[0] for x in zip(objectChar.schemeList, evalList) if x[1] == bestEval]
        # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
        if len(objectChar.schemeList) == 1:
            # 理论上把字根的二进制表示放进去才完备，但除了 C 输入要用到之外都不用，先不写
            # return tuple(
            #     {
            #         'name': objectChar.powerDict[x],
            #         'slice': x
            #     }
            #     for x in objectChar.schemeList[0])
            objectChar.bestScheme = tuple(objectChar.powerDict[x] for x in objectChar.schemeList[0])
        else:
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' % (objectChar.name, objectChar.schemeList))