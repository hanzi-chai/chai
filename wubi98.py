from Chai import Schema

# def newField(objectChar):
#     return ''

# def newSieve(objectChar, scheme):
#     return 1

wubi98 = Schema('wubi98')
# wubi98.setField('新域', newField)
# wubi98.setSieve('新筛', newSieve)
wubi98.run()

def output():
    """
    功能：利用字典 Schema.component 和树 Schema.tree 取码输出
    当方案对象经过解析器解析后，可用于拆分取码输出
    嵌套拆字功能，用于处理「字」数据库
    这里的功能是将嵌套结构拆分到最细，最细则是文数据库中的基础字/部件
    """
    codeList = []
    # 对于全部字集的每个名义字
    for nameChar in wubi98.charList:
        if nameChar in wubi98.component: # 如果字在「文」中
            scheme = wubi98.component[nameChar] # 索引用户字根拆分列
        else: # 否则按嵌套拆分拆开
            componentTree = wubi98.tree[nameChar]
            componentList = componentTree.flatten()
            # 对于拆出的每个基础字，索引出其用户字根拆分列，最后组合起来
            scheme = sum((wubi98.component[component] for component in componentList), tuple())
        if len(scheme) > 4: # 如果拆出的字根多于4个
            scheme = scheme[:3] + scheme[-1:] # 取前3尾1
        code = ''.join(wubi98.rootSet[root['name']] for root in scheme)
        codeList.append((nameChar, code))
    wubi98.codeList = codeList

output()

print('幂集用时：', wubi98.gpdTime)
print('拆分用时：', wubi98.decTime)
print('择优用时：', wubi98.selTime)

with open('preset/wubi98/result.yaml', 'w', encoding='utf-8') as f: # 写进文件
    for nameChar, code in wubi98.codeList:
        f.write('%s\t%s\n' % (nameChar, code))