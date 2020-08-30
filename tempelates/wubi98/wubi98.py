from pychai import ChaiClassical, Char

# 继承父类，实现编码方法。
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
            if (not char.struct) or char.struct not in 'hz':
                structTypeNum = 2   # 杂合型
            elif char.struct == 'h':
                structTypeNum = 1   # 左右型
            else:
                structTypeNum = 0   # 上下型
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

# 实例化拆分对象
wubi98 = Wubi('wubi98')
# 拆分
wubi98.genScheme()
# 编码
wubi98.encode()
# 输出编码表
wubi98.output()
# 输出拆分表
wubi98.output(outputSchemaResult=True)
