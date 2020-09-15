from .data_loader import load,loadFromPackage
WEN = loadFromPackage('wen.yaml')
ZI = loadFromPackage('zi.yaml')
TOPOLOGY = loadFromPackage('topology.yaml', withNumbers=False)