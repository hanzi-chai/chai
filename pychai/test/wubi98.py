from .. import ChaiClassical, Char, UnitChar

class Wubi(ChaiClassical):
    def encodeChar(self, char: Char) -> None:
        l = len(char.scheme)
        if l == 1:
            charName = char.name
            root = char.scheme[0]
            rootName = root.name
            keycode = self.rootKeymap[rootName]
            # 单根字中的键名字，击四次该键，等效于取四次该字根
            if charName in '王土大木工目日口田山禾白月人金言立水火之已子女又幺':
                keycode = keycode * 4
            # 单根字中的单笔画字，取码为双击该键加上两个 L
            elif charName in '一丨丿丶乙':
                keycode = keycode * 2 + 'll'
            # 普通成字字根，报户口 + 一二笔(+末笔)
            else:
                for stroke in root.strokeList[:2]:
                    keycode += self.rootKeymap[stroke.type]
                if len(root.strokeList) > 2:
                    lastStroke = root.strokeList[-1]
                    keycode += self.rootKeymap[lastStroke.type]
            char.keycode = keycode
        elif l < 4:    # 不足4根要加识别码
            keycode = ''
            # 先把字根取码
            for root in char.scheme:
                keycode += self.rootKeymap[root.name]
            # 建立识别码的键位映射，用二维数组表示
            structKeyRef = [
            #末笔 横   竖  撇   点  折
                ['g','h','t','y','n'], # 左右
                ['f','j','r','u','b'], # 上下
                ['d','k','e','i','v']  # 杂合
            ]
            structTypeNum = 0
            if (not char.struct) or char.struct not in 'hpz':
                structTypeNum = 2   # 杂合型
            elif char.struct == 'h':
                structTypeNum = 0   # 左右型
            else:
                structTypeNum = 1   # 上下型
            # 最后一笔的笔划号「12345」对应「横竖撇点折」
            lastStrokeTypeNum = self.storkeClassifier[char.strokeList[-1].type]
            keycode += structKeyRef[structTypeNum][lastStrokeTypeNum-1]
            char.keycode = keycode
        else:
            keycode = ''
            for root in char.scheme[:3]:
                keycode += self.rootKeymap[root.name]
            keycode += self.rootKeymap[char.scheme[-1].name]
            char.keycode = keycode

wubi98 = Wubi('wubi98', 'pychai/test/')
wubi98.genScheme()
char = wubi98.charDict['不']
print([uc.name for uc in char.scheme])
print(wubi98.rootKeymap['石上'])
# wubi98.encode()
# wubi98.output()

# originalDict={}
# with open("pychai/test/wubi98.dict-original.txt",mode="r",encoding="utf-8") as file:
#     for line in file:
#         char,code=line.strip('\n').split('\t')
#         originalDict[char]=code
# def scheme_toStrList(list_):
#     return ["{%s}" % unitChar.name for unitChar in list_]


# mistakeInfos = []
# for charName,chaiKeycode in wubi98.keycodeResultDict.items():
#     char = wubi98.charDict[charName]
#     orginalKeycode = originalDict[charName]
#     if chaiKeycode != orginalKeycode:
#         scheme_strList = scheme_toStrList(char.scheme)
#         possibleScheme=''
#         if isinstance(char, UnitChar):
#             possibleScheme = char.possibleSchemeList
#         mistakeInfo = [
#             '字符：%s' % char.name,
#             '字符结构：%s' % char.struct,
#             '字符末笔：%s' % char.strokeList[-1].type,
#             '原码：%s' % orginalKeycode,
#             '编码：%s' % chaiKeycode,
#             '可行拆分：%s' % possibleScheme,
#             '最终拆分：%s' % ''.join(scheme_strList),
#             ]
#         mistakeInfos.append('\n'.join(mistakeInfo))
# print('\n\n'.join(mistakeInfos))
# print(mistakeInfos.__len__())