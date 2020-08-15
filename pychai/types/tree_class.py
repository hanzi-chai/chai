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
            if node.first == None:
                componentList.append(node.name)
            else:
                stack.extend([node.second, node.first])
        return componentList

    def flatten_with_complex(self, complexRootList):
        """
        输入：树
        输出：将所有嵌套列表展开，并删去结构操作符，但保留合体字根！
        """
        stack = [self]
        componentList = []
        while stack:
            node = stack.pop()
            if node.first == None or node.name in complexRootList:
                componentList.append(node.name)
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