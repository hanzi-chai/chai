'''读取数据模块'''
# TODO: 把 load 改写成操作数据库的模块
from logging import DEBUG, FileHandler, getLogger
from os.path import dirname, exists, join
from pickle import load
from re import compile as RE
from sqlite3 import connect
from typing import Dict, List, Tuple

from yaml import BaseLoader, SafeLoader
from yaml import load as loadyaml

from ..base import Component, Compound, Stroke
from .build import buildCorner, buildTopology


def _path(relativePath):
    return join(dirname(__file__), relativePath)

def loadData(withTopology=False, withCorner=False) -> Tuple[Dict[str, Component], Dict[str, Compound]]:
    databasePath = _path('../data/main')
    database = connect(databasePath)
    cursor = database.cursor()
    strokeDataPattern = RE(r'(?<=\d)(?=M)')
    COMPONENTS = {}
    for row in cursor.execute('SELECT name, gb, pinyin, feature, svg FROM main WHERE operator IS NULL;'):
        name, inGB, pinyinString, featureString, svgString = row
        pinyinList = [] if pinyinString is None else pinyinString.split(',')
        featureList = featureString.split(',')
        svgList = strokeDataPattern.split(svgString)
        strokeList = [Stroke(feature, svg) for feature, svg in zip(featureList, svgList)]
        COMPONENTS[name] = Component(name, strokeList, None, inGB=inGB, pinyinList=pinyinList)
    if withTopology:
        topologyPath = _path('../data/topology')
        if not exists(topologyPath): buildTopology(COMPONENTS, topologyPath)
        with open(topologyPath, 'rb') as f: TOPOLOGIES = load(f)
        for name, component in COMPONENTS.items():
            component.topologyMatrix = TOPOLOGIES[name]
    if withCorner:
        cornerPath = _path('../data/corner')
        if not exists(cornerPath): buildCorner(COMPONENTS, cornerPath)
        with open(cornerPath, 'rb') as f: CORNERS = load(f)
        for name, component in COMPONENTS.items():
            component.corner = CORNERS[name]
    COMPOUNDS = {}
    compoundData = cursor.execute('SELECT name, gb, pinyin, operator, first, second, mix FROM main WHERE operator IS NOT NULL;').fetchall()
    while compoundData:
        row = compoundData.pop(0)
        name, inGB, pinyinString, operator, firstChildName, secondChildName, mix = row
        pinyinList = [] if pinyinString is None else pinyinString.split(',')
        firstChild = COMPONENTS.get(firstChildName, COMPOUNDS.get(firstChildName))
        secondChild = COMPONENTS.get(secondChildName, COMPOUNDS.get(secondChildName))
        if firstChild and secondChild:
            COMPOUNDS[name] = Compound(name, operator, firstChild, secondChild, mix, inGB=inGB, pinyinList=pinyinList)
        else:
            compoundData.append(row)
    return COMPONENTS, COMPOUNDS

def stdout(path):
    return open(path, 'w', encoding='utf-8')

def loadComponentsDependencies(characterNames: List[str]):
    pass

def loadCompoundsDependencies(characterNames: List[str]):
    pass
