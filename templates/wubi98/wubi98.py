'''
实现五笔
'''

from pychai import Sequential, Character

class Wubi98(Sequential):
    '''
    叶类
    '''

    def _encode(self, character: Character) -> None:
        scheme = character.scheme
        name = character.name
        l = len(scheme)
        if l == 1:
            root = scheme[0]
            key = self.rootMap[root.name]
            # 单根字中的键名字，击四次该键
            if name in '王土大木工目日口田山禾白月人金言立水火之已子女又幺':
                code = key * 4
            # 单根字中的单笔画字，取码为双击该键加上两个 L
            elif name in '一丨丿丶乙':
                code = key * 2 + 'll'
            # 普通成字字根，报户口 + 一二笔(+末笔)
            else:
                code = key
                for stroke in root.strokeList[:2]:
                    code += self.rootMap[stroke.feature]
                if len(root.strokeList) > 2:
                    lastStroke = root.strokeList[-1]
                    code += self.rootMap[lastStroke.feature]
            character.code = code
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
            character.code = code
        else:
            usefulScheme = scheme[:3] + scheme[-1:]
            character.code = ''.join([self.rootMap[root.name] for root in usefulScheme])

# 实例化拆分对象
wubi98 = Wubi98('templates/wubi98/wubi98.config.yaml')
wubi98.chai('templates/wubi98/wubi98.result.yaml')
