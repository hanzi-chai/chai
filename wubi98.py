from Chai import Schema

wubi98 = Schema('wubi98')
wubi98.run()

for nameChar in wubi98.charList:
    if nameChar in wubi98.component:
        # 如果字是基本部件，则获取字根拆分
        scheme = wubi98.component[nameChar]
    else:
        # 否则先按嵌套拆分拆开对于拆出的每个基础字，索引出其用户字根拆分列，最后组合起来
        componentTree = wubi98.tree[nameChar]
        componentList = componentTree.flatten()
        scheme = sum((wubi98.component[component] for component in componentList), tuple())
    if len(scheme) > 4: scheme = scheme[:3] + scheme[-1:]
    code = ''.join(wubi98.rootSet[root['name']] for root in scheme)
    wubi98.codeList.append((nameChar, code))

wubi98.output()