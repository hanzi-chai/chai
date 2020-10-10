'''
'''

from typing import Tuple, List, Dict
from ..base import Singlet, Degenerator, Selector
from ..preset import *

def buildClassifier(config) -> Dict[str,int]:
    strokeClassifier: Dict[str, int] = {}
    for strokeTypeNum, strokeNames in config['classifier'].items():
        for strokeName in strokeNames:
            strokeClassifier[strokeName] = int(strokeTypeNum)
    return strokeClassifier

def buildDegenerator(config) -> Degenerator:
    fieldDict = {
        '笔画序列': featureList,
        '笔画序列（简）': primitiveFeatureList,
        '笔画拓扑': topologyList
    }
    if any(fieldName not in fieldDict for fieldName in config['degenerator']):
        raise ValueError('未定义的退化函数')
    return Degenerator([fieldDict[fieldName] for fieldName in config['degenerator']])

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

def buildDegeneracy(CONFIG, COMPONENTS, COMPOUNDS) -> Tuple[List[Component], List[str]]:
    '''
    功能：解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
    输出：用户字根索引字典 degeneracy 、键位索引字典 rootKeymap
    '''
    # 退化字根到字根的映射，用于构建 powerDict
    rootList = []
    compoundRootList = []
    rootNameList = sum([list(x) for x in CONFIG['mapper'].values()], [])
    for rootName in rootNameList:
        # 字根是「文」数据中的一个部件
        if rootName in COMPONENTS:
            root = COMPONENTS[rootName]
            rootList.append(root)
        # 字根不是「文」数据库中的部件，但用户定义了它
        elif rootName in CONFIG['aliaser']:
            aliasData = CONFIG['aliaser'][rootName]
            source = COMPONENTS[aliasData['source']]
            indexList = aliasData['indexList']
            root = source.fragment(rootName, indexList)
            rootList.append(root)
        elif rootName in COMPOUNDS:
            compoundRootList.append(rootName)
        elif rootName in CONFIG['classifier']:
            relatedFeatureList = CONFIG['classifier'][rootName]
            for feature in relatedFeatureList:
                root = Singlet(feature)
                rootList.append(root)
        else:
            raise ValueError(f'不能识别的字根：{rootName}')
    return rootList, compoundRootList
