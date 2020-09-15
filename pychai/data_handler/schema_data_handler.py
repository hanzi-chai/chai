from typing import Tuple,Dict
from pychai.data import load, loadFromPackage, WEN
from pychai.classes import Stroke, UnitChar, Degenerator, Selector
from pychai.preset_function import *

def expandAliaser(aliaserValueList) -> list:
    """
    功能：展开形如 [1, ..., 6] 的省略式的笔画索引列
    输入：笔画索引列 indexList
    输入：展开后的笔画索引列 returnList ，形如 [1, 2, 3, 4, 5, 6]
    """
    l = len(aliaserValueList)
    i = 0
    while i < l:
        if aliaserValueList[i] == '...':
            end = int(aliaserValueList[i+1])
            replaceList = range(aliaserValueList[i-1]+1, end)
            aliaserValueList[i:i+1] = replaceList
            l_replaceList = len(replaceList)
            i = i + l_replaceList
            l = l - 1 + l_replaceList
        else:
            aliaserValueList[i] = int(aliaserValueList[i])
            i += 1
    return aliaserValueList

def checkCompleteness(classifier) -> None:
    """
    功能：检查笔画定义完整性
    输入：笔画定义字典 classifier 形如{type:[strokes]}
    输出：若有缺失定义，发起错误，打印缺失笔画列 lostStrokes 形如 [strokes]
    """
    allstrokes = [
        '横', '提', '竖', '竖钩', '撇', '点', '捺',
        '横钩', '横撇', '横折', '横折钩', '横斜钩', '横折提', '横折折',
        '横折弯', '横撇弯钩', '横折弯钩', '横折折撇', '横折折折', '横折折折钩',
        '竖提', '竖折', '竖弯', '竖弯钩', '竖折撇', '竖折折钩', '竖折折',
        '撇点', '撇折', '弯钩', '斜钩'
        ]
    userStrokeTypes = []
    # 读取用户对笔画的大类进行的自定义
    for strokeTypeList in classifier.values():
        userStrokeTypes.extend(strokeTypeList)
    userStrokeTypesSet = set(userStrokeTypes)
    # 校验是否所有单笔画都有定义
    lostStrokes = [x for x in allstrokes if x not in userStrokeTypesSet]
    if lostStrokes:
        raise ValueError('未定义的笔画：%s' % str(lostStrokes))

def loadSchemaData(schemaName: str, path: str='') -> dict:
    try:
        schemaData = load('%s%s.schema.yaml' % (path, schemaName), withNumbers=False)
    except FileNotFoundError:
        raise ValueError('您所指定的方案文件「%s.schema.yaml」不存在' % schemaName)
    if 'classifier' in schemaData:
        checkCompleteness(schemaData['classifier'])
    if 'aliaser' in schemaData:
        aliaser = schemaData['aliaser']
        for component in aliaser:
            indexList = aliaser[component][1]
            aliaser[component][1] = expandAliaser(indexList) # 展开省略式
    return schemaData

def build_strokeClassifier(schemaData) -> Dict[str,int]:
    strokeClassifier: Dict[str,int] = {}
    for strokeTypeNum, strokeNames in schemaData['classifier'].items():
        for strokeName in strokeNames:
            strokeClassifier[strokeName] = int(strokeTypeNum)
    return strokeClassifier

def build_degenerator(schemaData) -> Degenerator:
    degeneratorDict = {
        '笔画序列': getStrokeList,
        '笔画序列（简）': getStrokeListSimplified,
        '笔画拓扑': getTopoList
    }
    degenerator = Degenerator()
    for degeneratorName in schemaData['degenerator']:
        if degeneratorName not in degeneratorDict:
            raise ValueError("未定义的退化函数")
        else:
            degenerator.fields[degeneratorName] = degeneratorDict[degeneratorName]
    return degenerator

def build_selector(schemaData) -> Selector:
    sieveDict = {
        '根少优先': schemeLen,
        '笔顺优先': schemeOrder,
        '能连不交、能散不连': schemeTopo,
        '取大优先': schemeBias
    }
    selector = Selector()
    for sieveName in schemaData['selector']:
        if sieveName not in sieveDict:
            raise ValueError("未定义的择选函数")
        else:
            selector.sieves[sieveName] = sieveDict[sieveName]
    return selector

def generate_rootKeymap_degeneracy(
    schemaData,
    charDict,
    degenerator) -> Tuple[Dict[str, str], Dict[str, UnitChar]]:
    """
    功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
    输出：用户字根索引字典 degeneracy 、键位索引字典 rootKeymap
    """
    # TODO: 添加二笔式的字根处理。11代表两横等等。
    rootKeymap: Dict[str, str] = {} # 字根名到键位的映射，用于取码时键位索引
    degeneracy: Dict[str, UnitChar] = {} # 退化字根到字根的映射，用于构建 powerDict
    # complexRootList =[] # TODO:合体字根的处理
    allRoots = sum([list(x) for x in schemaData['mapper'].values()], [])
    for key, rootList in schemaData['mapper'].items():
        for rootName in rootList:
            # 是单笔画字根
            if rootName in schemaData['classifier']:
                for strokeType in schemaData['classifier'][rootName]:
                    rootKeymap[strokeType] = key
                    if strokeType not in ['竖折', '横钩', '横斜钩']:
                        strokeList = [Stroke([strokeType, None])]
                        degeneracy[strokeType] = UnitChar(strokeType, strokeList)
                    else:
                        degeneracy[strokeType] = charDict[strokeType]
            # 字根是「文」数据中的一个部件
            elif rootName in WEN:
                rootKeymap[rootName] = key
                char = charDict[rootName]
                characteristicString = degenerator(char)
                degeneracy[characteristicString] = char
                char.scheme = (char,)
            # 字根不是「文」数据库中的部件，但用户定义了它
            elif rootName in schemaData['aliaser']:
                rootKeymap[rootName] = key
                source, indexer = schemaData['aliaser'][rootName]
                l = len(WEN[source])
                sliceNum = sum(1 << (l - int(index) - 1)
                    for n, index in enumerate(indexer))
                strokeList = [Stroke(WEN[source][int(index)]) for index in indexer]
                char = UnitChar(rootName, strokeList, sourceName=source, sourceSlice=sliceNum)
                characteristicString = degenerator(char)
                degeneracy[characteristicString] = char
            # TODO:这种情况对应着合体字根，暂不考虑，等写嵌套的时候再写
            # elif root in ZI:
            #     complexRootList.append(root)
    return (rootKeymap, degeneracy)