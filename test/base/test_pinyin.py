from pychai import Pinyin, StandardPinyin, FixedZeroPinyin, FlexibleZeroPinyin

def cases():
    return [x + '1' for x in ['yin', 'yao', 'you', 'ye',
    'wu', 'wo', 'wei', 'wen',
    'yuan', 'yue',
    'a', 'er', 'n', 'm', 'ng',
    'ju', 'lü', 'liu', 'gui', 'zhun',
    ]]

def test_standard():
    pinyinList = [StandardPinyin(string) for string in cases()]
    assert [pinyin.sheng for pinyin in pinyinList] == ['零齐', '零齐', '零齐', '零齐', '零合', '零合', '零合', '零合', '零撮', '零撮', '零开', '零开', '零开', '零开', '零开', 'j', 'l', 'l', 'g', 'zh']
    assert [pinyin.yun for pinyin in pinyinList] == ['in', 'iao', 'iou', 'ie', 'u', 'uo', 'uei', 'uen', 'üan', 'üe', 'a', 'er', 'n', 'm', 'ng', 'ü', 'ü', 'iou', 'uei', 'uen']

def test_fixedZero():
    pinyinList = [FixedZeroPinyin(string) for string in cases()]
    assert [pinyin.sheng for pinyin in pinyinList] == ['y', 'y', 'y', 'y', 'w', 'w', 'w', 'w', 'y', 'y', '零', '零', '零', '零', '零', 'j', 'l', 'l', 'g', 'zh']
    assert [pinyin.yun for pinyin in pinyinList] == ['in', 'ao', 'ou', 'e', 'u', 'o', 'ei', 'en', 'uan', 'ue', 'a', 'er', 'n', 'm', 'ng', 'u', 'ü', 'iu', 'ui', 'un']

def test_flexibleZero():
    pinyinList = [FlexibleZeroPinyin(string) for string in cases()]
    assert [pinyin.sheng for pinyin in pinyinList] == ['y', 'y', 'y', 'y', 'w', 'w', 'w', 'w', 'y', 'y', '零a', '零e', '零o', '零o', '零o', 'j', 'l', 'l', 'g', 'zh']
    assert [pinyin.yun for pinyin in pinyinList] == ['in', 'ao', 'ou', 'e', 'u', 'o', 'ei', 'en', 'uan', 'ue', 'a', 'er', 'n', 'm', 'ng', 'u', 'ü', 'iu', 'ui', 'un']
