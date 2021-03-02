# TODO: 将此模块改写成读取 config ，辅助 chai 生成对象、读取数据的模块。
from typing import Dict

from yaml import SafeLoader
from yaml import load as loadyaml

from ..core.chai import Chai


def setupConfig(configPath: str) -> Chai:
    pass

def loadConfig(path) -> Dict:
    with open(path, encoding='utf-8') as file:
        config = loadyaml(file, SafeLoader)
    if 'classifier' in config:
        checkClassifierCompleteness(config['classifier'])
    if 'aliaser' in config:
        aliaser = config['aliaser']
        for _, data in aliaser.items():
            indexList = data['indexList']
            data['indexList'] = expandIndexList(indexList) # 展开省略式
    return config

def buildClassifier(config) -> Dict[str,int]:
    strokeClassifier: Dict[str, int] = {}
    for strokeTypeNum, strokeNames in config['classifier'].items():
        for strokeName in strokeNames:
            strokeClassifier[strokeName] = int(strokeTypeNum)
    return strokeClassifier

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

def checkClassifierCompleteness(classifier) -> None:
    '''检查笔画定义完整性

    :param classifier: 笔画定义字典，形如`{type:[strokes]}`
    :return: `None`。若有缺失定义，发起错误，打印缺失笔画列 lostStrokes 形如 [strokes]
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

def expandIndexList(aliaserValueList) -> list:
    '''展开形如`[1, ..., 6]`的省略式的笔画索引列

    :param aliaserValueList: 笔画索引列，形如`[1, ..., 5]`或`[1, 2, 3]`
    :return: 展开后的笔画索引列，形如`[1, 2, 3, 4, 5, 6]`
    '''
    output = []
    for index, item in enumerate(aliaserValueList):
        if isinstance(item, int):
            output.append(item)
        else:
            output.extend(list(range(
                aliaserValueList[index - 1] + 1, aliaserValueList[index + 1])))
    return output

        # for rootNameList in config['mapper'].values():
        #     for rootName in rootNameList:
        #         # 字根是「文」数据中的一个部件
        #         if rootName in self.components:
        #             root = self.components[rootName]
        #             self.componentRoots[rootName] = root
        #         # 字根不是「文」数据库中的部件，但用户定义了它
        #         elif rootName in config['aliaser']:
        #             aliasData = config['aliaser'][rootName]
        #             source = self.components[aliasData['source']]
        #             indexList = aliasData['indexList']
        #             root = source.fragment(rootName, indexList)
        #             self.componentRoots[rootName] = root
        #         elif rootName in self.compounds:
        #             self.compoundRoots[rootName] = None
        #         elif rootName in config['classifier']:
        #             relatedFeatureList = config['classifier'][rootName]
        #             for feature in relatedFeatureList:
        #                 root = Component.singlet(feature)
        #                 self.componentRoots[feature] = root
        #         else:
        #             raise ValueError(f'不能识别的字根：{rootName}')
