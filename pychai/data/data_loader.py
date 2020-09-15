import yaml
import pkgutil

def load(path, withNumbers=True):
    """
    功能：从当前工作目录中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    """
    return yaml.load(open(path, encoding='utf-8'), Loader=yaml.SafeLoader if withNumbers else yaml.BaseLoader)

def loadFromPackage(path, withNumbers=True):
    """
    功能：从模块包中加载 YAML 数据库
    输入：路径 path
    输出：yaml 解析器加载后的数据
    """
    return yaml.load(pkgutil.get_data(__package__, path).decode(), Loader=yaml.SafeLoader if withNumbers else yaml.BaseLoader)


