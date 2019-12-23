欢迎使用汉字自动拆分系统「拆」！

# 开始使用

「拆」的数据库为 YAML 文档，请安装解析库：

```bash
pip install PyYAML
```

# 代码结构

- `拆.py` 是自动拆分的入口程序；
- `文.yaml` 是基本部件的笔画信息表，来源于文泉驿；
- `字.yaml` 是将其他汉字分解为基本部件的信息表；
- `preset/` 是本系统内置的方案集，目前包括 98 五笔。

# 说明

## 数据库

1. 基础数据（暂定）：基础字根控制点列数据 文.yaml，嵌套字数据 字.yaml
2. 用户方案（暂定）：字根设定集 dict.yaml、补充嵌套字数据 alias.yaml、解析方案 schema.yaml

## 处理对象

1. 对象笔画 Stroke：带有笔画名、控制点列描述的对象
2. 名义字 nameChar：字名、字根名
2. 对象字 objectChar：含有名义字、对象笔画列等信息的对象
3. 方案 Schema：用于加载数据并解析方案的对象，用户直接面向的对象

## 主要功能函数

1. 退化函数 degenerate
    - 功能：将对象字的笔画列进行降维，形成退化的可散列对象
    - 输入：对象字 objectChar
    - 输出：退化字 degenChar
2. 用户字根索引生成函数 dict_parse
    - 功能：按「文」数据解析出退化的用户字根，建立退化字根到字根的字典、字根到键位的字典
    - 输入：基础数据、用户方案
    - 输出：用户字根索引字典 degeneracy 、键位索引字典 rootSet
3. 幂集生成函数 get_power_dict
    - 功能：解析出基础字的所有有效切片，构造切片到用户对象字的字典
    - 输入：对象字 objectChar
    - 输出：将带幂集字典 powerDict 传给对象字 objectChar
4. 拆分器 decomposer
    - 功能：解析出在给定字根集下对象字的所有有效的拆分
    - 输入：带 powerDict 的对象字 objectChar
    - 输出：将可能拆分列 schemeList 传给对象字 objectChar
5. 估值函数 evaluator
    - 功能：对一个拆分进行估值
    - 输入：一个拆分 scheme
    - 输出：数 schemeEval
6. 优化函数 optimizer
    - 功能：找出估值列中的最值
    - 输入：拆分列的估值列
    - 输出：估值列的最值 bestEval
7. 选择函数 select
    - 功能：利用估值函数对一个拆分进行估值，然后利用优化函数将最优化的拆分筛选出来
    - 输入：带 schemeList 的对象字 objectChar
    - 输出：将在择优逻辑下最优拆分 bestScheme 传给对象字 objectChar
8. 基础字拆分索引生成器 wen_parse
    - 功能：解析出「文」数据库中字按拆分逻辑及用户定义字根拆分出的拆分列建立文数据库中字到拆分列的字典
    - 输入：基础数据、用户方案
    - 输出：基础字拆分索引字典 component
9. 取码函数（暂定） output
    - 功能：当方案对象经过解析后，通过迭代「字」中名义字，拆解嵌套表并取码，从而输出码表

## 拆分逻辑顺序

1. 读取基础数据库和用户方案数据
2. 按「文」数据退化用户字根，生成用户字根索引字典
    - 注，当用户字根不在文中时，用户应该在Alias中定义该字根
3. 将「文」中基础字按用户字根拆开，生成基础字拆分索引字典
4. 将「字」中的嵌套字迭代拆成基础字，从基础字拆分索引器中索引出以用户字根组成的拆分列
5. 对拆分列索引键位，完成取码

## `拆.py` 功能

1. 实例化一个方案解析器 `schema = chai.Schema()`
2. 加载基础数据 `schema.load_base()`
    - 基础数据暂时位于与chai.py同级目录
3. 加载用户方案 `schema.load_schema(方案名)`
    - 用户方案暂时位于chai.py目录\preset\方案名\
    - 分别是dict.yaml、alias.yaml、schema.yaml
4. 解析方案 `schema.parse()`
5. 取码 `schema.output()`
6. 设置退化函数 `schema.set_degen_func(退化函数)`
7. 添加选择器 `schema.set_selector(选择器名称, 估值函数, 优化函数)`