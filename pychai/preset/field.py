'''
预置退化映射组件
'''

from ..base import Stroke, Component, Fragment

def featureList(component: Component):
    '''
    功能：退化函数组件，提取出一个对象字的笔画序列
    输入：对象字
    输出：降维的可散列类对象
    '''
    return ' '.join([stroke.feature for stroke in component.strokeList])

def primitiveFeatureList(component: Component):
    simplifier = {
        '竖钩': '竖',
        '竖弯': '竖弯钩',
        '横折钩': '横折',
        '提': '横',
        '捺': '点',
    }
    return ' '.join([simplifier.get(stroke.feature, stroke.feature) for stroke in component.strokeList])

def topologyList(component: Component):
    '''
    功能：退化函数组件，提取出一个对象字的拓扑
    输入：对象字
    输出：一个 n(n-1)/2 长度的字符串，n 为笔段个数
    '''
    topology = component.topologyMatrix
    if isinstance(component, Fragment):
        indexList = component.indexList
        topologyMatrix = component.source.topologyMatrix
        nestedList = [
            [
                relation for nrelation, relation in enumerate(row)
                if nrelation in indexList
            ]
            for nrow, row in enumerate(topologyMatrix)
            if nrow in indexList
        ]
    else:
        nestedList = topology
    image = ' '.join(' '.join(x) for x in nestedList)
    # 给这对字根添加额外的区分：
    if component.name in ['囗', '囱框']:
        image += '囗'
    return image
