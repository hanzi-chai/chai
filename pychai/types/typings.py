from typing import NewType,Dict,List,Tuple,Union

# globle basic types
StrokeType = NewType('笔画',str)  # 笔画，如：'横'，'坚'，'撇'，'点'等等
StrokeTypeCategory = NewType('笔画分类',Union[int,str]) # 笔画分类，如：1代表'横'，5代表'折'等等
Root = NewType('基础字根',str) # pychai系统内建中用于拆分的基础字根
NestChar = NewType('嵌套字',str) # 嵌套字
NameChar = NewType('名义字',str) # 字符串型式的字

# data basic types
StrokeRelation = NewType('笔画关系',str)
# data
# TODO:描述下面的any
Zi = Dict[NestChar,List[any]]
Wen = Dict[Root,any]
Topology = Dict[Root,List[List[StrokeRelation]]]

# schema basic types
SieveName = NewType('择优方法',str)
Key = NewType('键位',str) # 键盘键位，用于建立字根对应键位的映射
UserRoot = NewType('用户字根',Union[int,str])
RootStroke = NewType('名义字笔划',int) # 用于表示名义字中的笔划
FieldName = NewType('退化方法',str)

# schema
Degenerator = List[FieldName]
Selector = List[SieveName]
Classifier = Dict[StrokeTypeCategory,List[StrokeType]]
Mapper = Dict[Key,List[UserRoot]]
Aliaser = Dict[Root,Tuple[NameChar,List[RootStroke]]]
