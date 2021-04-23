from os.path import join, dirname, exists
from typing import List, Dict, Tuple
from logging import getLogger, FileHandler, DEBUG
from re import compile as RE
from sqlite3 import connect
from pickle import load
from yaml import BaseLoader, SafeLoader, load as loadyaml
from .build import buildTopology, buildCorner
from ..base import Stroke, Component, Compound
from ..logger import DecompositionFormatter

def _path(relativePath):
    return join(dirname(__file__), relativePath)

def loadData(withTopology=False, withCorner=False) -> Tuple[Dict[str, Component], Dict[str, Compound]]:
    databasePath = _path('../data/main')
    database = connect(databasePath)
    cursor = database.cursor()
    strokeDataPattern = RE(r'(?<=\d)(?=M)')
    COMPONENTS = {}
    for row in cursor.execute('SELECT name, gb, pinyin, feature, svg FROM main WHERE operator IS NULL;'):
        name, inGB, pinyinString, featureString, svgString = row
        pinyinList = [] if pinyinString is None else pinyinString.split(',')
        featureList = featureString.split(',')
        svgList = strokeDataPattern.split(svgString)
        strokeList = [Stroke(feature, svg) for feature, svg in zip(featureList, svgList)]
        COMPONENTS[name] = Component(name, strokeList, None, inGB=inGB, pinyinList=pinyinList)
    if withTopology:
        topologyPath = _path('../data/topology')
        if not exists(topologyPath): buildTopology(COMPONENTS, topologyPath)
        with open(topologyPath, 'rb') as f: TOPOLOGIES = load(f)
        for name, component in COMPONENTS.items():
            component.topologyMatrix = TOPOLOGIES[name]
    if withCorner:
        cornerPath = _path('../data/corner')
        if not exists(cornerPath): buildCorner(COMPONENTS, cornerPath)
        with open(cornerPath, 'rb') as f: CORNERS = load(f)
        for name, component in COMPONENTS.items():
            component.corner = CORNERS[name]
    COMPOUNDS = {}
    compoundData = cursor.execute('SELECT name, gb, pinyin, operator, first, second, mix FROM main WHERE operator IS NOT NULL;').fetchall()
    while compoundData:
        row = compoundData.pop(0)
        name, inGB, pinyinString, operator, firstChildName, secondChildName, mix = row
        pinyinList = [] if pinyinString is None else pinyinString.split(',')
        firstChild = COMPONENTS.get(firstChildName, COMPOUNDS.get(firstChildName))
        secondChild = COMPONENTS.get(secondChildName, COMPOUNDS.get(secondChildName))
        if firstChild and secondChild:
            COMPOUNDS[name] = Compound(name, operator, firstChild, secondChild, mix, inGB=inGB, pinyinList=pinyinList)
        else:
            compoundData.append(row)
    return COMPONENTS, COMPOUNDS

def loadConfig(path) -> Dict:
    with open(path, encoding='utf-8') as file:
        config = loadyaml(file, SafeLoader)
    if 'classifier' in config:
        checkCompleteness(config['classifier'])
    if 'aliaser' in config:
        aliaser = config['aliaser']
        for _, data in aliaser.items():
            indexList = data['indexList']
            data['indexList'] = expandAliaser(indexList) # 展开省略式
    return config

def loadReference(path):
    with open(path, encoding='utf-8') as file:
        return loadyaml(file, BaseLoader)

def stdout(path):
    return open(path, 'w', encoding='utf-8')

def stderr(path):
    MSG_FMT = '%(message)s'

    logger = getLogger('binaryDictLogger')
    handler = FileHandler(path, mode='w', encoding='utf-8')
    handler.setLevel(DEBUG)
    handler.setFormatter(DecompositionFormatter(MSG_FMT))
    logger.addHandler(handler)
    return logger

def expandAliaser(aliaserValueList) -> list:
    '''展开形如 [1, ..., 6] 的省略式的笔画索引列
    参数：
        笔画索引列，形如 [1, ..., 5] 或 [1, 2, 3]

    输出：
        展开后的笔画索引列，形如 [1, 2, 3, 4, 5, 6]
    '''
    output = []
    for index, item in enumerate(aliaserValueList):
        if isinstance(item, int):
            output.append(item)
        else:
            output.extend(list(range(
                aliaserValueList[index - 1] + 1, aliaserValueList[index + 1]
            )))
    return output

def checkCompleteness(classifier) -> None:
    '''检查笔画定义完整性

    参数：
        classifier 笔画定义字典，形如{type:[strokes]}

    输出：
        若有缺失定义，发起错误，打印缺失笔画列 lostStrokes 形如 [strokes]
    '''
    allFeatureList = [
        '横', '提', '竖', '竖钩', '撇', '点', '捺',
        '横钩', '横撇', '横折', '横折钩', '横斜钩', '横折提', '横折折',
        '横折弯', '横撇弯钩', '横折弯钩', '横折折撇', '横折折折', '横折折折钩',
        '竖提', '竖折', '竖弯', '竖弯钩', '竖折撇', '竖折折钩', '竖折折',
        '撇点', '撇折', '弯钩', '斜钩'
    ]
    # 读取用户对笔画的大类进行的自定义
    definedFeatureList = sum(classifier.values(), [])
    # 校验是否所有单笔画都有定义
    lostFeatureList = [feature for feature in allFeatureList if feature not in definedFeatureList]
    if lostFeatureList:
        raise ValueError('未定义的笔画：%s' % str(lostFeatureList))
