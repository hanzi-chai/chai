from pychai.base.character import Component


def strokeFeatureEqual(strokeFeature1: str, strokeFeature2: str):
    '''笔画类型比对，相同为 True ，不相同为 False 。其中「点」和「捺」视为相同。
    '''
    if strokeFeature1 != strokeFeature2:
        if strokeFeature1 == '点':
            return strokeFeature2 == '捺'
        elif strokeFeature1 == '捺':
            return strokeFeature2 == '点'
        return False
    return True
