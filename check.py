from pychai import Sequential, Character

def loadDict(path: str):
    r = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            char, code = line.strip().split('\t')
            r[char] = code
    return r

original = loadDict('wubi98.original.txt')

class Wubi98(Sequential):
    '''
    叶类
    '''

    def _encode(self, character: Character) -> str:
        scheme = character.scheme
        name = character.name
        l = len(scheme)
        if l == 1:
            root = scheme[0]
            # 单根字中的键名字，击四次该键
            if name in '王土大木工目日口田山禾白月人金言立水火之已子女又幺':
                code = self.rootMap[root.name] * 4
            # 单根字中的单笔画字，取码为双击该键加上两个 L
            elif name in '一丨丿丶乙':
                code = self.rootMap[root.name] * 2 + 'll'
            # 普通成字字根，报户口 + 一二笔(+末笔)
            else:
                code = self.rootMap[root.name]
                for stroke in root.strokeList[:2]:
                    code += self.rootMap[stroke.feature]
                if len(root.strokeList) > 2:
                    lastStroke = root.strokeList[-1]
                    code += self.rootMap[lastStroke.feature]
        elif l < 4:    # 不足4根要加识别码
            code = ''.join([self.rootMap[root.name] for root in scheme])
            # 识别码
            if character.operator == 'h':
                identifierList = 'ghtyn'
            elif character.operator == 'z':
                identifierList = 'fjrub'
            else:
                identifierList = 'dkeiv'
            lastRoot = scheme[-1]
            lastStroke = lastRoot.strokeList[-1]
            # 末根末笔的笔划号「12345」对应「横竖撇点折」
            lastStrokeCategory = self.classifier[lastStroke.feature]
            code += identifierList[lastStrokeCategory - 1]
        else:
            usefulScheme = scheme[:3] + scheme[-1:]
            code = ''.join([self.rootMap[root.name] for root in usefulScheme])
        return code

    def debug(self):
        self.getComponentScheme()
        self.getCompoundScheme()
        self.encode()
        diff = 0
        total = 0
        for name, cpn in self.COMPONENTS.items():
            if name in original:
                total +=1
                if original[name] != cpn.code:
                    print(name+':')
                    print('original:'+original[name])
                    print('result:'+cpn.code)
                    print('scheme:'+' '.join([ c.name for c in cpn.scheme]))
                    diff += 1
        print(total)
        print(diff)

# 实例化拆分对象
wubi98 = Wubi98('templates/wubi98/wubi98.config.yaml')
wubi98.debug()

