'''拼音对象模块'''
from abc import ABC
from functools import cached_property
from re import compile as RE
from re import sub
from typing import Tuple


class Pinyin(ABC):
    regularize = {}
    splitter = None

    def __init__(self, pinyinString: str):
        self.string = pinyinString
        self.diao = pinyinString[-1]
        shengyun = pinyinString[:-1]
        for k, v in self.regularize.items():
            shengyun = sub(k, v, shengyun)
        self.sheng, self.yun = self.splitter.split(shengyun)

    @cached_property
    def initial(self) -> str: return self.string[0]

    @cached_property
    def shengyun(self) -> Tuple: return (self.sheng, self.yun)

    @cached_property
    def shengyundiao(self) -> Tuple: return (self.sheng, self.yun, self.diao)

class StandardPinyin(Pinyin):
    '''
    参考 https://zh.m.wikisource.org/zh-hans/%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E6%96%B9%E6%A1%88。
    '''
    regularize = {
        '([zcs])i': r'\1i1', # 舌尖元音 ɿ
        '(h)i': r'\1i2', # 舌尖元音 ʅ
        '^([aoe])': r'零开\1', # 开口呼
        '^(m|n|ng)$': r'零开\1', # 鼻音韵母算开口呼
        'w(u)': r'零合\1', # 合口呼 wu
        'w([aoe])': r'零合u\1', # 合口呼其他
        'y(i)': r'零齐\1', # 齐齿呼 yi yin ying
        'y([aoe])': r'零齐i\1', # 齐齿呼 ya yan yang ye you yong
        'y(u)': r'零撮ü', # 撮口呼
        '([jqx])u|([nl])v': r'\1ü',
        'iu': 'iou',
        'ui': 'uei',
        'un': 'uen'
    }
    splitter = RE(r'(?<=[bpmfdtnlgkhjqxzcsrh开合齐撮])(?=[aeiouünm])')

class FixedZeroPinyin(Pinyin):
    '''
    固定零声母，如微软双拼
    '''
    regularize = {
        '^([aoe])': r'零\1',
        '^(m|n|ng)$': r'零\1',
        'v': r'ü',
    }
    splitter = RE(r'(?<=[bpmfdtnlgkhjqxzcsryw零])(?=[aeiouünm])')

class FlexibleZeroPinyin(Pinyin):
    '''
    不固定零声母，如自然码双拼、小鹤双拼
    '''
    regularize = {
        '^([aoe])': r'零\1\1',
        '^(m|n|ng)$': r'零o\1',
        'v': r'ü',
    }
    splitter = RE(r'(?<=[bpmfdtnlgkhjqxzcsryw])(?=[aeiouünm])|(?<=零[aoe])')
