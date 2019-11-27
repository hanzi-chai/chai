import yaml

WEN = yaml.load(open('文.yaml'), Loader=yaml.BaseLoader)
ALIAS = yaml.load(open('文.alias.yaml'), Loader=yaml.BaseLoader)
BH = yaml.load(open('GB笔画.yaml'), Loader=yaml.BaseLoader)
DY = yaml.load(open('preset/wubi98.dict.yaml'), Loader=yaml.BaseLoader)['stroke']
WEN_ = {}
with open('文.raw.yaml') as f:
    wenl = f.readlines()[2:]
    for i in wenl:
        if i[1] == ':':
            current = i[0]
            WEN_[current] = []
        else:
            content = i[5:-1]
            try:
                strokeType, data = content.split(',', 1)
                strokeType = strokeType.strip()
                data = '[' + data.strip()
                WEN_[current].append([strokeType] + eval(data))
            except Exception:
                WEN_[current].append([content.strip(']')])

d = {}
for key, value in DY.items():
    for v in value:
        d[v] = key

WRONG = []

for component, strokeList in WEN.items():
    if component in BH:
        wqy = ''.join([d[stroke[0]] for stroke in strokeList])
        if wqy != BH[component]: WRONG.append((component, wqy, BH[component]))
    else:
        source = ALIAS[component][0]
        indexList = [int(x) for x in ALIAS[component][1]]
        sourceStrokeList = WEN_[source]
        wqy = ''.join([d[stroke[0]] for stroke in strokeList])
        gb = ''.join([num for index, num in enumerate(BH[source]) if index in indexList])
        if wqy != gb: WRONG.append((component, wqy, gb))

with open('文.error.yaml', 'w') as f:
    for item in WRONG:
        char, wrong, right = item
        f.write('%s: {错误: %s, 正确: %s}\n' % (char, wrong, right))
