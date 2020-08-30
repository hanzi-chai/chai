from .chai_abstract import ChaiAbstract

class ChaiErbi(ChaiAbstract):
    # TODO: 根据抽象类结构修改Erbi
    def genRoot(self, objectChar):
        """
        功能：二笔的 powerDict 只含顺序取笔
        """
        for k in range(2, objectChar.charlen + 1):
            characteristicString = self.degenerator(Char('', objectChar.strokeList[:k], sourceName=objectChar.name, sourceSlice=((1 << k)-1)))
            if self.degeneracy.get(characteristicString):
                objectChar.root = self.degeneracy.get(characteristicString)

    def run(self):
        self.category = {}
        for category, strokeTypeList in self.schema['classifier'].items():
            for strokeType in strokeTypeList:
                self.category[strokeType] = category
        self.component = {}
        for nameChar in self.wen:
            strokeList = [Stroke(stroke) for stroke in self.wen[nameChar]]
            objectChar = Char(nameChar, strokeList)
            objectChar.root = None
            strokeCategoryList = [self.category[stroke.type] for stroke in strokeList]
            self.genRoot(objectChar)
            if objectChar.root:
                self.component[nameChar] = (objectChar.root.name, strokeCategoryList)
            else:
                self.component[nameChar] = (''.join(strokeCategoryList[:2]), strokeCategoryList)
