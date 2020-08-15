import yaml
from pychai.types import *
# TODO: 调整读取基本数据模块
WEN: Wen = yaml.safe_load(open('wen.yaml',encoding='utf-8'))
ZI: Zi = yaml.safe_load(open('zi.yaml',encoding='utf-8'))
TOPOLOGY: Topology = yaml.load(open('topology.yaml',encoding='utf-8'),Loader=yaml.BaseLoader)