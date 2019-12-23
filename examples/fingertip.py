from Chai import Schema

# 加载方案
fingertip = Schema('fingertip')
# 运行拆分
fingertip.run()

def output():
    """
    功能：根据 Chai 运行生成的结果输出码表
    输入：封装在方案对象 fingertip 中的
        - 基本部件拆分字典 fingertip.component
        - 嵌套树 fingertip.tree
    输出：将 GB 字集内全部汉字的编码列表封装在 fingertip.codeList 中
    """
    fingertip.codeList = []
    # 对于全部字集的每个名义字
    for nameChar in fingertip.charList:
        # 如果字是一个基本部件，则索引用户字根拆分列
        if nameChar in fingertip.component:
            scheme = fingertip.component[nameChar][:4]
        else:
        # 按嵌套拆分拆开
            tree = fingertip.tree[nameChar]
            first = tree.first
            second = tree.second
            if first in fingertip.component:
                if second in fingertip.component: # 二分字
                    scheme = fingertip.component[first][:2] + fingertip.component[second][:2]
                else:
                    scheme = fingertip.component[first][:1] + \
                        fingertip.component[second.first.veryFirst()][:1] + \
                        fingertip.component[second.second.veryFirst()][:2]
            else:
                if second in fingertip.component: # 三分字
                    scheme = fingertip.component[first.first.veryFirst()][:1] + \
                        fingertip.component[first.second.veryFirst()][:1] + \
                        fingertip.component[second][:2]
                else:
                    scheme = fingertip.component[first.first.veryFirst()][:1] + \
                        fingertip.component[first.second.veryFirst()][:1] + \
                        fingertip.component[second.first.veryFirst()][:1] + \
                        fingertip.component[second.second.veryFirst()][:1]
        if len(scheme) < 4: # 末码补全
            scheme = (scheme + (scheme[-1:] * 2))[:4]
        code = ''.join(fingertip.rootSet[root['name']] for root in scheme)
        fingertip.codeList.append((nameChar, code))

output()

with open('preset/fingertip/result.yaml', 'w', encoding='utf-8') as f: # 写进文件
    for nameChar, code in fingertip.codeList:
        f.write('%s\t%s\n' % (nameChar, code))