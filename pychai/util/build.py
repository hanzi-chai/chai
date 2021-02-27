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

def buildRoots(CONFIG, COMPONENTS: Dict[str, Component], COMPOUNDS: Dict[str, Compound]):
    #退化字根到字根的映射，用于构建 powerDict
    componentRoot: Dict[str, Component] = {}
    compoundRoot: Dict[str, None] = {}
    for rootNameList in CONFIG['mapper'].values():
        for rootName in rootNameList:
            # 字根是「文」数据中的一个部件
            if rootName in COMPONENTS:
                root = COMPONENTS[rootName]
                componentRoot[rootName] = root
            # 字根不是「文」数据库中的部件，但用户定义了它
            elif rootName in CONFIG['aliaser']:
                aliasData = CONFIG['aliaser'][rootName]
                source = COMPONENTS[aliasData['source']]
                indexList = aliasData['indexList']
                root = source.fragment(rootName, indexList)
                componentRoot[rootName] = root
            elif rootName in COMPOUNDS:
                compoundRoot[rootName] = None
            elif rootName in CONFIG['classifier']:
                relatedFeatureList = CONFIG['classifier'][rootName]
                for feature in relatedFeatureList:
                    root = Component.singlet(feature)
                    componentRoot[feature] = root
            else:
                raise ValueError(f'不能识别的字根：{rootName}')
    return componentRoot, compoundRoot

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
