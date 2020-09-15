from pychai.classes import Char, UnitChar, NestedChar, Stroke
from typing import Dict

def build_objChar_dict(wen, zi) -> Dict[str, Char]:
    charDict = {}
    # 将 wen 中数据生成基本单元字 UnitChar 对象，绑定到 charDict
    for unitCharName, strokeInfos in wen.items():
        strokeList = [ Stroke(strokeInfo) for strokeInfo in strokeInfos]
        charDict[unitCharName] = UnitChar(unitCharName, strokeList)
    # 套娃前的准备工作
    def generate_nestedChar(charName: str, nestedList):
        """
        功能：把zi.yaml中的数据生成嵌套字，记入 charDict 中
        输入：
            charName 嵌套字名称
            nestedList 嵌套列表
        """
        def nestedList_item_handler(item) -> Char:
            """
            功能：处理嵌套列表的元素
            输入：嵌套列表中，结构符后面的嵌套元素
            输出：对象字
            """
            # 若 item 是字符串，则是一个字
            if isinstance(item, str):
                # charDict 有实例就直接返回（因为 wen 的基本单元字已经存在 charDict里面了
                if item in charDict:
                    return charDict[item]
                # 不在 charDict 里面，但在 zi 里面，就生成然后从 charDict 中取出来返回
                elif item in zi:
                    generate_nestedChar(item, zi[item])
                    return charDict[item]
                # 既不在 charDict 里面（也就是不在 wen 里面），也不在 zi 里面，就是未定义的字符。
                else:
                    raise Exception("「%s」嵌套字符未找到" % item)
            # 若 item 不是字符串，则是一个List。是没有名字的嵌套结构（意义上等同一个「无名」的字）。
            else:
                # 用嵌套结构起一个临时名子
                charName = ''.join([str(x) for x in item])
                generate_nestedChar(charName, item)
                return charDict[charName]
            pass
        struct = nestedList[0]
        firstComponent = nestedList_item_handler(nestedList[1])
        secondComponent = nestedList_item_handler(nestedList[2])
        thirdComponent = None
        if len(nestedList) == 4:
            third = nestedList[3]
            if not isinstance(third,int):
                thirdComponent = nestedList_item_handler(third)
            else:
                # TODO: 嵌套结构中的笔顺信息暂时没有处理
                pass
        nestedChar=NestedChar(charName, struct, firstComponent, secondComponent,
            thirdComponent)
        charDict[charName]=nestedChar
        pass
    # 开始套娃，将 zi 中数据生成嵌套字 NestedChar 对象，绑定到 charDict
    for charName, nestedList in zi.items():
        generate_nestedChar(charName, nestedList)
    return charDict
