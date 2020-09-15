from .char_data_handler import build_objChar_dict
from .schema_data_handler import \
    loadSchemaData, \
    build_degenerator, \
    build_selector, \
    generate_rootKeymap_degeneracy, \
    build_strokeClassifier
from .data_loader import load,loadFromPackage
WEN = loadFromPackage('wen.yaml')
ZI = loadFromPackage('zi.yaml')
TOPOLOGY = loadFromPackage('topology.yaml', withNumbers=False)