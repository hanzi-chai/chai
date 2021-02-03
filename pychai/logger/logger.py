from logging import Formatter, LogRecord
from typing import Dict
from ..base import Component

class DecompositionFormatter(Formatter):
    def format(self, record: LogRecord):
        component: Component = record.msg
        output = f'{component.name}:\n\n#二进制表示:\n'
        for binary, root in component.binaryDict.items():
            record.msg = f'- {binary:0{component.length}b} : {root.name}'
            output += f'{super().format(record)}\n'
        output += '\n#筛选过程:\n'
        for info in component.infoList:
            sieveName = info['name']
            output += f'- {sieveName}:\n'
            schemeAndScoreList = info['schemeAndScoreList']
            for scheme, score in schemeAndScoreList:
                descriptor = ', '.join(f'{binary:0{component.length}b}[{component.binaryDict[binary].name}]' for binary in scheme)
                output += f'  - {descriptor}: {score}\n'
        return output
