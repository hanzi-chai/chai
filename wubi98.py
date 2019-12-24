from Chai import Schema

wubi98 = Schema('wubi98')
wubi98.run()

for nameChar in wubi98.charList:
    if nameChar in wubi98.component:
        scheme = wubi98.component[nameChar]
    else:
        componentList = wubi98.tree[nameChar].flatten()
        scheme = sum((wubi98.component[component] for component in componentList), tuple())
    if len(scheme) > 4: scheme = scheme[:3] + scheme[-1:]
    code = ''.join(wubi98.rootSet[root['name']] for root in scheme)
    wubi98.encoder[nameChar] = code

wubi98.output()