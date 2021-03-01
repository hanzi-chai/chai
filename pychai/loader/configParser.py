# TODO: 将此模块改写成读取 config ，辅助 chai 生成对象、读取数据的模块。
from pickle import dump
from typing import Dict

from ..base import Component, Compound, Selector
from ..preset import *
from .corner import findCorner
from .topology import findTopology


def buildClassifier(config) -> Dict[str,int]:
    strokeClassifier: Dict[str, int] = {}
    for strokeTypeNum, strokeNames in config['classifier'].items():
        for strokeName in strokeNames:
            strokeClassifier[strokeName] = int(strokeTypeNum)
    return strokeClassifier

def buildSelector(config) -> Selector:
    sieveDict = {
        '根少优先': length,
        '笔顺优先': order,
        '能连不交、能散不连': topology,
        '取大优先': bias
    }
    if any(sieveName not in sieveDict for sieveName in config['selector']):
        raise ValueError('未定义的退化函数')
    return Selector([sieveDict[sieveName] for sieveName in config['selector']])

def buildRootMap(config) -> Dict[str, str]:
    # 字根名到键位的映射，用于取码时键位索引
    rootMap: Dict[str, str] = {}
    for key, rootList in config['mapper'].items():
        for rootName in rootList:
            # 是单笔画字根
            if rootName in config['classifier']:
                for strokeType in config['classifier'][rootName]:
                    rootMap[strokeType] = key
            else:
                rootMap[rootName] = key
    return rootMap

def buildTopology(COMPONENTS, topologyPath) -> None:
    TOPOLOGIES = {
        componentName: findTopology(component)
        for componentName, component in COMPONENTS.items()
    }
    with open(topologyPath, 'wb') as file:
        dump(TOPOLOGIES, file)

def buildCorner(COMPONENTS, cornerPath) -> None:
    CORNERS = {
        componentName: findCorner(component)
        for componentName, component in COMPONENTS.items()
    }
    with open(cornerPath, 'wb') as file:
        dump(CORNERS, file)

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

def loadReference(path):
    with open(path, encoding='utf-8') as file:
        return loadyaml(file, BaseLoader)

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
