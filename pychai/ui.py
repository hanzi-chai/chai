from .tools import loadFromPackage
from .objects import Tree
import shutil
import os

def example(schemaName):
    try:
        shutil.copy('%s/preset/%s.schema.yaml' % (os.path.dirname(__file__), schemaName), '%s/%s.schema.yaml' % (os.getcwd(), schemaName))
        shutil.copy('%s/preset/%s.py' % (os.path.dirname(__file__), schemaName), '%s/%s.py' % (os.getcwd(), schemaName))
    except Exception:
        print('您所请求的示例方案「%s」不存在。')

def lookup(sourceChar: str, numList: list):
    WEN = loadFromPackage('文.yaml')
    ZI = loadFromPackage('字.yaml')
    if sourceChar in WEN:
        print('恭喜！您现在可以为该字根起一个名字，在 mapper 中添加这个字根的名字，并在 aliaser 中注册，语法如下：\n【名字】: [%s, %s]' % (sourceChar, str(numList).replace("'", '')))
    elif sourceChar in ZI:
        print('您提供的汉字「%s」不是基本部件，它的结构为：%s。请尝试将您需要的字根定位到这些基本部件中，然后重新查询。' % (sourceChar, str(ZI[sourceChar]).replace("'", '')))
    else:
        print('您提供的汉字「%s」不在 GB 字集内。请您使用常用汉字查询字根。' % sourceChar)
