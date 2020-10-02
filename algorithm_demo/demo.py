import random
import time
from typing import Dict, List, Callable

class Component():
    '''
    测试用的Component对象

    属性：(累了)

    '''
    def __init__(self, stroke_list: str, topo_str: str):
        self.stroke_list = stroke_list
        self.topo_str = topo_str
        self.length = len(stroke_list)
        self.topo_slice_cache: Dict[int, str] = { 1 : '' }

    def get_topo_slice(self, index_list: List[int]):
        binary_code = self.index_list_to_binary_code(index_list)
        if binary_code in self.topo_slice_cache:
            return self.topo_slice_cache[binary_code]
        topo_slice = ''
        length = len(index_list)
        for n in range(1, length):
            index = index_list[n]
            offset = int(index * (index - 1) / 2)
            for before_n in range(0, n):
                topo_slice += self.topo_str[offset + index_list[before_n]]
        self.topo_slice_cache[binary_code] = topo_slice
        return topo_slice

    def get_topo_simple_slice(self, end_index: int):
        binary_code = 2 ** (end_index + 1) - 1
        if binary_code in self.topo_slice_cache:
            return self.topo_slice_cache[binary_code]
        topo_slice = self.topo_str[ : int((end_index * (end_index + 1)) / 2)]
        self.topo_slice_cache[binary_code] = topo_slice
        return topo_slice

    def index_list_to_binary_code(self, index_list: List[int]):
        length = self.length
        binary_code: int = 0
        for index in index_list:
            binary_code += 1 << (length - index - 1)
        return binary_code

    def clear_topo_slice_cache(self):
        self.topo_slice_cache = { 1 : '' }

    def __str__(self):
        return f'list:{self.stroke_list}\ntopo:{self.topo_str}'

    def __eq__(self, other):
        if not isinstance(other,Component):
            return NotImplemented
        return self.stroke_list == other.stroke_list and self.topo_str == other.topo_str

def find_slice_v1(component: Component, root: Component):
    '''check topo on each step'''
    component_length = component.length
    root_length = root.length
    result: List[int] = []
    if component_length < root_length:
        return result
    component_stroke_list = component.stroke_list
    root_stroke_list = root.stroke_list
    root_first_stroke = root_stroke_list[0]
    length_limit = component_length - root_length + 1
    valid_index_lists: List[List[int]] = []
    for component_index in range(0, length_limit):
        if component_stroke_list[component_index] == root_first_stroke:
            valid_index_lists.append([component_index])
    if len(valid_index_lists) == 0:
        return result
    else:
        for root_index in range(1,root_length):
            new_valid_index_lists: List[List[int]] = []
            end_loop = length_limit + root_index
            for index_list in valid_index_lists:
                for component_index in range(index_list[-1]+1,end_loop):
                    if component_stroke_list[component_index] == root_stroke_list[root_index]:
                        new_index_list = index_list + [component_index]
                        if component.get_topo_slice(new_index_list) == root.get_topo_simple_slice(root_index):
                            new_valid_index_lists.append(new_index_list)
            if len(new_valid_index_lists) == 0:
                return result
            else:
                valid_index_lists = new_valid_index_lists
    for index_list in valid_index_lists:
        result.append(component.index_list_to_binary_code(index_list))
    return result

def find_slice_v1_1(component: Component, root: Component):
    '''v1基础上加上提前终止判断语句'''
    component_length = component.length
    root_length = root.length
    result: List[int] = []
    if component_length < root_length:
        return result
    component_stroke_list = component.stroke_list
    root_stroke_list = root.stroke_list
    root_first_stroke = root_stroke_list[0]
    length_limit = component_length - root_length + 1
    valid_index_lists: List[List[int]] = []
    for component_index in range(0, length_limit):
        if component_stroke_list[component_index] == root_first_stroke:
            valid_index_lists.append([component_index])
    if len(valid_index_lists) == 0:
        return result
    else:
        for root_index in range(1,root_length):
            new_valid_index_lists: List[List[int]] = []
            end_loop = length_limit + root_index
            for index_list in valid_index_lists:
                not_found: bool = True
                for component_index in range(index_list[-1]+1,end_loop):
                    if component_stroke_list[component_index] == root_stroke_list[root_index]:
                        not_found = False
                        new_index_list = index_list + [component_index]
                        if component.get_topo_slice(new_index_list) == root.get_topo_simple_slice(root_index):
                            new_valid_index_lists.append(new_index_list)
                if not_found:
                    break
            if len(new_valid_index_lists) == 0:
                return result
            else:
                valid_index_lists = new_valid_index_lists
    for index_list in valid_index_lists:
        result.append(component.index_list_to_binary_code(index_list))
    return result

def find_slice_v2(component: Component, root: Component):
    '''check topo on final stage'''
    component_length = component.length
    root_length = root.length
    result: List[int] = []
    if component_length < root_length:
        return result
    component_stroke_list = component.stroke_list
    root_stroke_list = root.stroke_list
    length_limit = component_length - root_length + 1
    root_first_stroke = root_stroke_list[0]
    valid_index_lists: List[List[int]] = []
    for component_index in range(0,length_limit):
        if component_stroke_list[component_index]==root_first_stroke:
            valid_index_lists.append([component_index])
    if len(valid_index_lists)==0:
        return result
    else:
        for root_index in range(1, root_length):
            new_valid_index_lists: List[List[int]] = []
            end_loop = length_limit + root_index
            for index_list in valid_index_lists:
                for component_index in range(index_list[-1] + 1,end_loop):
                    if component_stroke_list[component_index] == root_stroke_list[root_index]:
                        new_index_list = index_list + [component_index]
                        new_valid_index_lists.append(new_index_list)
            if len(new_valid_index_lists) == 0:
                return result
            else:
                valid_index_lists = new_valid_index_lists
    for index_list in valid_index_lists:
        if component.get_topo_slice(index_list) == root.topo_str:
            result.append(component.index_list_to_binary_code(index_list))
    return result

def find_slice_v2_1(component: Component, root: Component):
    '''v2基础上加上提前终止判断语句'''
    component_length = component.length
    root_length = root.length
    result: List[int] = []
    if component_length < root_length:
        return result
    component_stroke_list = component.stroke_list
    root_stroke_list = root.stroke_list
    length_limit = component_length - root_length + 1
    root_first_stroke = root_stroke_list[0]
    valid_index_lists: List[List[int]] = []
    for component_index in range(0,length_limit):
        if component_stroke_list[component_index]==root_first_stroke:
            valid_index_lists.append([component_index])
    if len(valid_index_lists)==0:
        return result
    else:
        for root_index in range(1, root_length):
            new_valid_index_lists: List[List[int]] = []
            end_loop = length_limit + root_index
            for index_list in valid_index_lists:
                not_found: bool = True
                for component_index in range(index_list[-1] + 1,end_loop):
                    if component_stroke_list[component_index] == root_stroke_list[root_index]:
                        not_found = False
                        new_index_list = index_list + [component_index]
                        new_valid_index_lists.append(new_index_list)
                if not_found:
                    break
            if len(new_valid_index_lists) == 0:
                return result
            else:
                valid_index_lists = new_valid_index_lists
    for index_list in valid_index_lists:
        if component.get_topo_slice(index_list) == root.topo_str:
            result.append(component.index_list_to_binary_code(index_list))
    return result


def find_all_valid_combinations(component: Component, roots: List[Component], find_slice_fn: Callable[[Component,Component],List[int]]):
    slice_binary_code_dict: Dict[int,Component] = {}
    for root in roots:
        slice_binary_code_list = find_slice_fn(component, root)
        for slice_binary_code in slice_binary_code_list:
            slice_binary_code_dict[slice_binary_code] = root
    slice_binary_code_list = list(slice_binary_code_dict.keys())
    slice_binary_code_list_length = len(slice_binary_code_list)
    result : List[List[Component]] = []
    if slice_binary_code_list_length == 0:
        return result
    slice_binary_code_list.sort(reverse=True)
    def inner(current_combination_state_binary_code: int,current_stroke_to_find: int, current_combination_list: List[Component], start_searching_from_index: int):
        not_found_current_stroke_to_find_flag = True
        while current_stroke_to_find!=0 and not_found_current_stroke_to_find_flag:
            for index in range(start_searching_from_index,slice_binary_code_list_length):
                binary_code = slice_binary_code_list[index]
                if current_stroke_to_find & binary_code != 0 and current_combination_state_binary_code & binary_code == 0:
                    not_found_current_stroke_to_find_flag = False
                    new_combination_state_binary_code = current_combination_state_binary_code + binary_code
                    new_combination_list = current_combination_list + [slice_binary_code_dict[binary_code]]
                    next_stroke_to_find = current_stroke_to_find >> 1
                    while next_stroke_to_find & new_combination_state_binary_code != 0:
                        next_stroke_to_find = next_stroke_to_find >> 1
                    if next_stroke_to_find==0:
                        result.append(new_combination_list)
                    else:
                        inner(new_combination_state_binary_code, next_stroke_to_find, new_combination_list, index + 1)
            if not_found_current_stroke_to_find_flag:
                current_stroke_to_find = current_stroke_to_find>>1
    inner(0, 1 << (component.length - 1), [], 0)
    return result


#### test utils
def random_stroke_list(n: int) -> str:
    '''随机生成n笔画字的笔画序列。笔画用数字字符串表示。

    参数：
        n：笔画序列长度

    输出：
        首位不为'0'的阿拉伯数字字符串，长度为 n 。
    '''
    return str(random.randint(10**(n-1),10**(n)-1))

def random_topo_str(n: int) -> str:
    '''随机生成 n 笔字的 topo 序列。等效于把 pychai 当中的 topologyMatrix 合成一串字符串。

    参数：
        n：笔画序列的长度

    输出：
        仅由'0','1','2'组成的字符串，长度为 (n*(n-1))/2
    '''
    return ''.join([ str(random.randint(0,2)) for _ in range(int((n*(n-1))/2))])

def build_random_components(stroke_length: int, how_many: int):
    '''批量生成随机的、属性不重复的 Component

    参数：
        stroke_length：生成 Component 的笔画长度。
        how_many：生成的个数

    输出：
        包含所有随机生成 Component 的列表
    '''
    components: List[Component] = [Component(random_stroke_list(stroke_length),random_topo_str(stroke_length))]
    count = 0
    while count<how_many:
        new_component = Component(random_stroke_list(stroke_length),random_topo_str(stroke_length))
        for component in components:
            if component==new_component:
                break
            else:
                components.append(new_component)
                count+=1
    return components

def test_slice_function_performance(components: List[Component], roots: List[Component], test_fn: Callable[[Component,Component],List[int]]):
    '''测试「取切片函数」运行效率的函数

    无输出。在控制台打印相关数据。

    参数：
        components：待拆分的字集合
        roots：字根集合
        test_fn：被测试的「取切片函数」
    '''
    total_times = len(components) * len(roots)
    success_times = 0
    failure_elapsed = 0
    success_elapsed = 0
    start = time.time()
    for component in components:
        for root in roots:
            t = time.time()
            result = test_fn(component,root)
            elapsed = time.time() - t
            if len(result)>0:
                success_times += 1
                success_elapsed += elapsed
            else:
                failure_elapsed += elapsed
    total_elapsed = time.time() - start
    failure_times = total_times - success_times
    success_avg = success_elapsed/success_times*1000000 if success_times!=0 else 0
    failure_avg = failure_elapsed/failure_times*1000000 if failure_times!=0 else 0
    print(f'success:{success_times}\nsuccess_avg:{success_avg}')
    print(f'failure:{total_times-success_times}\nfailure_avg:{failure_avg}')
    print(f'total_time_elapsed:{int(total_elapsed*1000)}ms, times:{total_times}')
    print()

def test_find_combination_function_performance(components: List[Component], roots: List[Component], test_fn: Callable[[Component,List[Component]],list]):
    '''测试「查找可行根组合函数」运行效率的函数

    输出耗时(ms)。并在控制台打印数据。

    参数：
        components：待拆字集合
        roots：字根集合
        test_fn：被测试的「查找可行根组合函数」

    输出：
        测试总用时(ms)
    '''
    success_elapsed = 0
    failure_elapsed = 0
    start = time.time()
    for component in components:
        t1 = time.time()
        r = test_fn(component,roots)
        elapsed = time.time() - t1
        if len(r)>0:
            success_elapsed += elapsed
        else:
            failure_elapsed += elapsed
    total_elapsed = time.time() - start
    print(f'total_time_elapsed:{int(total_elapsed*1000)}ms')
    print()
    return int(total_elapsed*1000)

def clear_all_cache(components: List[Component]):
    '''清除所有 component 的 topo 切片缓存'''
    for component in components:
        component.clear_topo_slice_cache()

def wrap1(component: Component,roots: List[Component]):
    return find_all_valid_combinations(component,roots,find_slice_v1)

def wrap2(component: Component,roots: List[Component]):
    return find_all_valid_combinations(component,roots,find_slice_v2)

def wrap3(component: Component,roots: List[Component]):
    return find_all_valid_combinations(component,roots,find_slice_v1_1)

def wrap4(component: Component,roots: List[Component]):
    return find_all_valid_combinations(component,roots,find_slice_v2_1)

def check_correctness():
    # 生成一个“天”字
    component = Component('横横撇点','散连交散连连')
    roots = [
        Component('横',''),         #根“一”
        Component('横横','散'),      #根“二”
        Component('撇点','连'),      #根“人”
        Component('横撇点','交连连'),  #根“大”
        Component('撇',''),          #根“丿”
        Component('点','')           #根“丶”
    ]
    print('-----v1-----')
    result = wrap1(component,roots)
    for scheme_list in result:
        print()
        for r in scheme_list:
            print(r.stroke_list)
    print('-----v2-----')
    result = wrap2(component,roots)
    for scheme_list in result:
        print()
        for r in scheme_list:
            print(r.stroke_list)
    print('-----v3-----')
    result = wrap3(component,roots)
    for scheme_list in result:
        print()
        for r in scheme_list:
            print(r.stroke_list)
    print('-----v4-----')
    result = wrap4(component,roots)
    for scheme_list in result:
        print()
        for r in scheme_list:
            print(r.stroke_list)

def performance_comparison_graph():
    # components = build_random_components(2,49) + build_random_components(3,76) + build_random_components(4,106) + \
    #     build_random_components(5,79) + build_random_components(6,55) + build_random_components(7,43) + \
    #     build_random_components(8,35) + build_random_components(9,18) + build_random_components(10,10) + \
    #     build_random_components(11,6)
    single_stroke_roots = [Component('1',''), Component('2',''), Component('3',''), Component('4',''), \
        Component('5',''), Component('6',''), Component('7',''), Component('8',''), Component('9',''), \
        Component('0','')]
    x = []
    time1 = []
    time2 = []
    time3 = []
    time4 = []
    for component_stroke_num in range(5,20):
        x.append(component_stroke_num)
        components = build_random_components(component_stroke_num,500)
        roots = single_stroke_roots + build_random_components(2,50) + build_random_components(3,50) + \
            build_random_components(4,50) + build_random_components(5,50)
        t1 = test_find_combination_function_performance(components,roots,wrap1)
        time1.append(t1)
        clear_all_cache(components)
        clear_all_cache(roots)
        t2 = test_find_combination_function_performance(components,roots,wrap2)
        time2.append(t2)
        clear_all_cache(components)
        clear_all_cache(roots)
        t3 = test_find_combination_function_performance(components,roots,wrap3)
        time3.append(t3)
        clear_all_cache(components)
        clear_all_cache(roots)
        t4 = test_find_combination_function_performance(components,roots,wrap4)
        time4.append(t4)
    import matplotlib.pyplot as plt
    plt.title('comparison')
    plt.plot(x,time1,color='green',label='v1')
    plt.plot(x,time2,color='blue',label='v2')
    plt.plot(x,time3,color='yellow',label='v3')
    plt.plot(x,time4,color='pink',label='v4')
    plt.legend()
    plt.xlabel('stroke num')
    plt.ylabel('time elapsed(ms)')
    plt.show()

#### run tests

# test1
# components = build_random_components(8,1000) + build_random_components(9,1000) + \
#     build_random_components(14,2000) + build_random_components(15,2000) + \
#     build_random_components(16,2000) + build_random_components(17,2000) + \
#     build_random_components(23,1000) + build_random_components(24,1000) + \
#     build_random_components(26,1000) + build_random_components(28,1000) + \
#     build_random_components(28,1000) + build_random_components(30,1000)
# single_stroke_roots = [Component('1',''), Component('2',''), Component('3',''), Component('4',''), \
#     Component('5',''), Component('6',''), Component('7',''), Component('8',''), Component('9',''), \
#     Component('0','')]
# roots = single_stroke_roots + build_random_components(2,50) + build_random_components(3,50) + \
#     build_random_components(4,60) + build_random_components(5,60)
# test_slice_function_performance(components,roots,find_slice_v1_check_topo_on_each_step)
# clear_all_cache(components)
# clear_all_cache(roots)
# test_slice_function_performance(components,roots,find_slice_v2_check_on_final_stage)
# clear_all_cache(components)
# clear_all_cache(roots)
# test_slice_function_performance(components,roots,v3)
# clear_all_cache(components)
# clear_all_cache(roots)
# test_slice_function_performance(components,roots,v4)

# test2
# check_correctness()

# test3
# performance_comparison_graph()
