from typing import List, Tuple, Union, Callable

from ....base import Component, Compound
from ..pictorial import Pictorial
from .corner import findCorner


class CornerCode(Pictorial):
    '''四角符号拆分器'''
    def __init__(self,
        components: List[Component],
        compounds: List[Compound],
        componentRoots: List[Component],
        compoundRoots: List[Compound],
        evaluators: Callable[[Component, Tuple[int, ...]],Union[int,Tuple[int, ...]]]):
        super().__init__(components, compounds, componentRoots, compoundRoots, evaluators)

    @staticmethod
    def findRoot(component, index, schemeBinary):
        binary = 1 << (component.length - index - 1)
        cornerRootBinary, = filter(lambda x: x & binary, schemeBinary)
        # TODO: 这个 root 是干嘛的
        root = component.binaryDict[cornerRootBinary]

    def generateComponentScheme(self, component: Component):
        if component.name in self.componentRoots:
            return (component,)
        schemeBinary = self.generateComponentSchemeBinary(component)
        scheme = tuple(component.binaryDict[x] for x in schemeBinary)
        lt, rt, lb, rb = map(CornerCode.findRoot, findCorner(component))
        component.scheme = {
            'all': scheme,
            'lt': lt,
            'rt': rt,
            'lb': lb,
            'rb': rb
        }

    def generateCompoundScheme(self, compound: Compound):
        scheme = super().generateCompoundScheme(compound)
        fstScheme = compound.firstChild.scheme
        scdScheme = compound.secondChild.scheme
        operator = compound.operator
        lt = fstScheme['lt']
        rt = fstScheme['rt'] if operator in 'hl' else scdScheme['rt']
        lb = fstScheme['lb'] if operator in 'zq' else scdScheme['lb']
        rb = fstScheme['lb'] if operator in 'hz' else scdScheme['lb']
        compound.scheme =  {
            'all': scheme,
            'lt': lt,
            'rt': rt,
            'lb': lb,
            'rb': rb
        }
