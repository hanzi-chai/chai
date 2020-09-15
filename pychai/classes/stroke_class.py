class Stroke():
    """
    笔画对象：
      - 类别（31 种）
      - 起始点
      - 绘制列表（1 个至 4 个绘制）
    注：类别和控制点详见
        https://github.com/lanluoxiao/Chai/wiki/1-%E3%80%8C%E6%96%87%E3%80% \
        8D%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83。
    """

    def __init__(self, obj: list):
        self.type = obj[0]
        self.start = obj[1]
        self.drawList = obj[2:]

    def __str__(self):
        return str(self.type) + ':' + str(self.drawList) + ' '