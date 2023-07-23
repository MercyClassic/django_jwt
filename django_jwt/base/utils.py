

def return_extra_attrs_func(func_info: dict):
    module = func_info.get('module')
    func_name = func_info.get('func_name')
    exec(f'from {module} import {func_name}')
    func = eval(func_name)
    return func
