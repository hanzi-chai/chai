class Stroke():
    
    """
    笔画对象：
      - 类别（31 种）
      - 控制点列表（2 个至 6 个）
    注：类别和控制点详见
        https://github.com/lanluoxiao/Chai/wiki/1-%E3%80%8C%E6%96%87%E3%80% \
        8D%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83。
    """
    
    def __init__(self, obj):
        self.type = obj[0]
        controlList = []
        for point in obj[1:]:
            controlList.append((int(point[0]), int(point[1])))
        self.controlList = controlList
    
    def __str__(self):
        return str(self.type) + ':' + str(self.controlList) + ' '


class Char():
    
    """
    汉字对象（对象字 objectChar）：
      - 名称（名义字 nameChar）
      - 笔画列表，每个元素是一个 Stroke 对象
    """
    
    def __init__(self, nameChar, strokeList):
        self.name = nameChar
        self.strokeList = strokeList
        self.charlen = len(strokeList)
    
    def __str__(self):
        strokeList = [str(stroke) for stroke in self.strokeList]
        return self.name + '{\n\t' + '\n\t'.join(strokeList) + '\n\t}'

class Tree():
    """
    树对象
    """

    def __init__(self, name, nestedList, zi):
        self.name = name
        if nestedList:
            self.structure = nestedList[0]
            first = nestedList[1]
            second = nestedList[2]
            if len(nestedList) == 4:
                self.cross = nestedList[-1]
            if isinstance(first, str):
                if first in zi:
                    self.first = Tree(first, zi[first], zi)
                else:
                    self.first = Tree(first, [], zi)
            else:
                self.first = Tree('', first, zi)
            if isinstance(second, str):
                if second in zi:
                    self.second = Tree(second, zi[second], zi)
                else:
                    self.second = Tree(second, [], zi)
            else:
                self.second = Tree('', second, zi)
        else:
            self.first = None
            self.second = None
            self.structure = ''

    def flatten(self):
        """
        输入：树
        输出：将所有嵌套列表展开，并删去结构操作符
        """
        stack = [self]
        componentList = []
        while stack:
            node = stack.pop()
            if isinstance(node, str):
                componentList.append(node)
            else:
                stack.extend([node.second, node.first])
        return componentList

    def veryFirst(self):
        """
        """
        node = self
        while node.first:
            node = node.first
        return node.name
    
    def verySecond(self):
        node = self
        while node.second:
            node = node.second
        return node.name
    
    def divisible(self):
        return bool(self.first)