from pkgutil import get_data
from typing import List, Dict
import yaml
from yaml import BaseLoader, SafeLoader
from ..base import Stroke, Component, Compound

def loadInternal(path, withNumbers=True):
    '''
    功能：从模块包中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    '''
    data = get_data(__package__, path).decode()
    loader = SafeLoader if withNumbers else BaseLoader
    return yaml.load(data, loader)

def loadExternal(path, withNumbers=True):
    '''
    功能：从模块包中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    '''
    loader = SafeLoader if withNumbers else BaseLoader
    with open(path, encoding='utf-8') as file:
        return yaml.load(file, loader)

def loadGB() -> List[str]:
    return loadInternal('../data/GB.yaml')

def loadComponents() -> Dict[str, Component]:
    data = loadInternal('../data/components.yaml')
    COMPONENTS = {}
    for name, componentData in data.items():
        strokeList = [Stroke(strokeData) for strokeData in componentData]
        COMPONENTS[name] = Component(name, strokeList)
    return COMPONENTS

def loadComponentsWithTopology() -> Dict[str, Component]:
    COMPONENTS = loadComponents()
    TOPOLOGIES = loadInternal('../cache/topology.yaml')
    for name, component in COMPONENTS.items():
        component.topologyMatrix = TOPOLOGIES[name]
    return COMPONENTS

def loadCompounds(COMPONENTS) -> Dict[str, Compound]:
    data = loadInternal('../data/compounds.yaml')
    COMPOUNDS = {}
    for name, compoundData in data.items():
        operator = compoundData['operator']
        firstChildName, secondChildName = compoundData['operandList']
        firstChild = COMPONENTS[firstChildName] if firstChildName in COMPONENTS else COMPOUNDS[firstChildName]
        secondChild = COMPONENTS[secondChildName] if secondChildName in COMPONENTS else COMPOUNDS[secondChildName]
        mix = compoundData.get('mix')
        COMPOUNDS[name] = Compound(name, operator, firstChild, secondChild, mix)
    return COMPOUNDS

def loadConfig(path) -> Dict:
    config = loadExternal(path)
    if 'classifier' in config:
        checkCompleteness(config['classifier'])
    if 'aliaser' in config:
        aliaser = config['aliaser']
        for _, data in aliaser.items():
            indexList = data['indexList']
            data['indexList'] = expandAliaser(indexList) # 展开省略式
    return config

def expandAliaser(aliaserValueList) -> list:
    '''
    功能：展开形如 [1, ..., 6] 的省略式的笔画索引列
    输入：笔画索引列 indexList
    输入：展开后的笔画索引列 returnList ，形如 [1, 2, 3, 4, 5, 6]
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
    '''
    功能：检查笔画定义完整性
    输入：笔画定义字典 classifier 形如{type:[strokes]}
    输出：若有缺失定义，发起错误，打印缺失笔画列 lostStrokes 形如 [strokes]
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
