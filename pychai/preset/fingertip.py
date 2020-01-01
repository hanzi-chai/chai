from pychai import Schema

# 加载方案
fingertip = Schema('fingertip')
# 运行拆分
fingertip.run()

for nameChar in fingertip.charList:
    # 如果字是一个基本部件，则索引用户字根拆分列
    if nameChar in fingertip.component:
        scheme = fingertip.component[nameChar][:4]
    else:
    # 按嵌套拆分拆开
        tree = fingertip.tree[nameChar]
        first = tree.first
        second = tree.second
        if not first.divisible():
            if not second.divisible(): # 二分字
                scheme = fingertip.component[first.name][:2] + fingertip.component[second.name][:2]
            else: # 三分字，前一后二
                scheme = fingertip.component[first.name][:1] + \
                fingertip.component[second.first.veryFirst()][:1] + \
                fingertip.component[second.second.veryFirst()][:2]
        else:
            if not second.divisible(): # 三分字，前二后一
                scheme = fingertip.component[first.first.veryFirst()][:1] + \
                fingertip.component[first.second.veryFirst()][:1] + \
                fingertip.component[second.name][:2]
            else: # 四分字
                scheme = fingertip.component[first.first.veryFirst()][:1] + \
                fingertip.component[first.second.veryFirst()][:1] + \
                fingertip.component[second.first.veryFirst()][:1] + \
                fingertip.component[second.second.veryFirst()][:1]
    if len(scheme) < 4: # 末码补全
        scheme = (scheme + (scheme[-1:] * 3))[:4]
    code = ''.join(fingertip.rootSet[objectRoot.name] for objectRoot in scheme)
    fingertip.encoder[nameChar] = code

fingertip.output()