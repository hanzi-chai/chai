import yaml

class SVG:
    """
    根据笔形数据，绘画出SVG
    """
    def __init__(self, nameChar:str, strokeList:list, color:str='red', thickness:int=10):
        """
        :param strokes: 一个列表，包含每个笔画的描述文本（例如：[撇, [m, 512 25], [q, 114, 236, -484, 965]]）
        :param color: 线条的颜色，是个字符串，例如："red" "#f00" "#00ff00"
        :param thickness: 线条的粗细，是个正数，单位为pixel。如：20
        """
        self.name = nameChar
        self.strokeList = strokeList
        self.color = color
        self.thickness = thickness

    def convert_path_label(self)->str:
        pathList = []
        for stroke in self.strokeList:
            commandList = []
            for command in stroke[1:]:
                commandStr = command[0] + ' '.join(list(map(str, command[1:])))
                commandList.append(commandStr)
            a = ' '.join(commandList)
            b = "  <path d='{}' fill='transparent' stroke='{}' stroke-width='{}px'/>".format(a, self.color, self.thickness)
            pathList.append(b)
        return '\n'.join(pathList)

    def get_svg_label(self)->str:
        """
        返回svg标签的字根，用于内嵌于html中。
        """
        return "<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='1000px' height='1000px'>\n%s\n</svg>" % self.convert_path_label()
    
    def output(self, path:str = None):
        """
        将svg文件保存为指定的本地文件。
        :param path: svg文件的路径
        """
        a = self.get_svg_label()
        r = "<?xml version='1.0' standalone='no'?>\n" \
            "<!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' \n" \
            "'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'>\n\n "+a
        if path == None: path = '%s.svg' % self.name
        with open(path, 'w', encoding='u8') as f:
            f.write(r)

if __name__ == "__main__":
    nameChar = '以'
    WEN = yaml.load(open('Chai/文.yaml'), Loader=yaml.SafeLoader)
    strokeList = WEN[nameChar]
    svg = SVG(nameChar, strokeList)
    svg.output()