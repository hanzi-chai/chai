from xml.etree.ElementTree import parse

f = open('GB.txt', encoding='utf-8', mode='r')
charDict = {line.strip('\r\n'): None for line in f}
f.close()

# print(chr(eval('0x7684')))

TTF = parse('苹方简极细.xml')
code2name = {}
for item in TTF.iterfind('cmap/cmap_format_4/map'):
    code = item.get('code')
    name = item.get('name')
    code2name[code] = name
name2text = {}
for item in TTF.iterfind('CFF/CFFFont/CharStrings/CharString'):
    name = item.get('name')
    pathList = item.text.strip().split('\n')[:-1]
    newPathList = []
    for path in pathList:
        argList = path.strip().split()
        newPath = argList[-1].replace('to', '') + '(' + ', '.join(argList[:-1]) + ')'
        newPathList.append(newPath)
    text = '; '.join(newPathList)
    name2text[name] = text.replace('1000, ', '')

for char in charDict:
    hexcode = str(hex(ord(char)))
    name = code2name[hexcode]
    text = name2text[name]
    charDict[char] = (hexcode, text)

outputList = sorted([(key, ) + value for key, value in charDict.items()], key=lambda x: eval(x[1]))

f = open('笔画路径信息.txt', encoding='utf-8', mode='w')
f.write('\n'.join('\t'.join(line) for line in outputList))
f.close()