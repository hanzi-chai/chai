'''
经典形码
'''

from typing import Dict, List, Tuple
from .chai import Chai
from ..base import Component, Compound

class Sequential(Chai):
    '''
    经典形码
    '''
    @staticmethod
    def findSliceV1(component: Component, root: Component):
        '''check topo on each step'''
        cpnStrokeList = component.strokeList
        rootStrokeList = root.strokeList
        cpnLength = len(cpnStrokeList)
        rootLength = len(rootStrokeList)
        result: List[int] = []
        if cpnLength < rootLength:
            return result
        rootFirstStroke = rootStrokeList[0]
        searchLengthLimit = cpnLength - rootLength + 1
        validIndexLists: List[List[int]] = []
        for cpnStrokeListIndex in range(0, searchLengthLimit):
            if cpnStrokeList[cpnStrokeListIndex].feature == rootFirstStroke.feature:
                validIndexLists.append([cpnStrokeListIndex])
        if len(validIndexLists) == 0:
            return result
        else:
            for rStrokeListIndex in range(1, rootLength):
                nextLevelValidIndexLists: List[List[int]] = []
                limit = searchLengthLimit + rStrokeListIndex
                for indexList in validIndexLists:
                    for cpnStrokeListIndex in range(indexList[-1]+1, limit):
                        if cpnStrokeList[cpnStrokeListIndex].feature == rootStrokeList[rStrokeListIndex].feature:
                            expandedIndexList = indexList + [cpnStrokeListIndex]
                            c_topo = component.getTopologyMatrixSlice(expandedIndexList)
                            r_topo = component.getTopologyMatrixSliceSimple(rStrokeListIndex)
                            if  Component.topologyMatrixToString(c_topo) == Component.topologyMatrixToString(r_topo):
                                nextLevelValidIndexLists.append(expandedIndexList)
                if len(nextLevelValidIndexLists) == 0:
                    return result
                else:
                    validIndexLists = nextLevelValidIndexLists
        for indexList in validIndexLists:
            result.append(component.indexListToBinaryCode(indexList))
        return result

    def findAllValidCombinations(self, component: Component):
        for root in self.rootList:
            sliceBinaryCodeList = Sequential.findSliceV1(component, root)
            for sliceBinaryCode in sliceBinaryCodeList:
                component.powerDict[sliceBinaryCode] = root
        sliceBinaryCodeList = list(component.powerDict.keys())
        sliceBinaryCodeListLength = len(sliceBinaryCodeList)
        result : List[Tuple[int,...]] = []
        if sliceBinaryCodeListLength == 0:
            return result
        sliceBinaryCodeList.sort(reverse=True)
        def inner(currentCombinationStateBinaryCode: int,currentStrokeToFind: int, currentCombinationTuple: Tuple[int,...], startSearchingFromIndex: int):
            notFoundFlag = True
            while currentStrokeToFind!=0 and notFoundFlag:
                for index in range(startSearchingFromIndex,sliceBinaryCodeListLength):
                    binaryCode = sliceBinaryCodeList[index]
                    if currentStrokeToFind & binaryCode != 0 and currentCombinationStateBinaryCode & binaryCode == 0:
                        notFoundFlag = False
                        newCombinationStateBinaryCode = currentCombinationStateBinaryCode + binaryCode
                        expandedCombinationTuple = currentCombinationTuple + (binaryCode,)
                        nextStrokeMask = currentStrokeToFind >> 1
                        while nextStrokeMask & newCombinationStateBinaryCode != 0:
                            nextStrokeMask = nextStrokeMask >> 1
                        if nextStrokeMask==0:
                            result.append(expandedCombinationTuple)
                        else:
                            inner(newCombinationStateBinaryCode, nextStrokeMask, expandedCombinationTuple, index + 1)
                if notFoundFlag:
                    currentStrokeToFind = currentStrokeToFind>>1
        inner(0, 1 << (len(component.strokeList) - 1), (), 0)
        return result

    def _getComponentScheme(self, component: Component) -> Tuple[Component, ...]:
        if component.name in self.rootMap:
            return (component,)
        else:
            component.schemeList = self.findAllValidCombinations(component)
            return self.selector(component)

    def _getCompoundScheme(self, compound: Compound) -> Tuple[Component, ...]:
        firstChild, secondChild = compound.firstChild, compound.secondChild
        return firstChild.scheme + secondChild.scheme
