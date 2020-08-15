"""读取*.schema.yaml配置文件用的工具"""
import yaml

def loadData(schemaName: str)->dict:
    try:
        data = yaml.load(open('%s.schema.yaml' % schemaName, encoding='utf-8'), \
                Loader=yaml.BaseLoader)
    except FileNotFoundError:
        try:
            data = yaml.load(open('preset_schema/%s/%s.schema.yaml' % schemaName, schemaName, \
                    encoding='utf-8'), Loader=yaml.BaseLoader)
        except FileNotFoundError:
            raise ValueError('您所指定的方案文件「%s.schema.yaml」不存在' % schemaName)
    if 'classifier' in data:
        checkClassifier(data['classifier'])
    if 'aliaser' in data:
        for component in data['aliaser']:
            indexList = aliaser[component][1]
            data[component][1] = expandAliaser(indexList) # 展开省略式
    return data

def expandAliaser(indexList: Sequence[Union[int,str]])->List[RootStroke]:
    """
    功能：展开形如 [1, ..., 6] 的省略式的笔画索引列
    输入：笔画索引列 indexList
    输入：展开后的笔画索引列 returnList ，形如 [1, 2, 3, 4, 5, 6]
    """
    for i in range(len(indexList)):
        if indexList[i] == '...':
            indexList[i:i+1] = range(indexList[i-1]+1,indexList[i+1])
            return indexList
    return indexList

def checkCompleteness(classifier: Classifier)->None:
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