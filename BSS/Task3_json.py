import json


# функция текущий элемент json-структуры возвращает в виде строки
# j_object - это текущий объект, current_tab - текущий отступ
def node_to_str(j_object, current_tab):
    # если текущий объект является списком, множеством или кортежем
    if (type(j_object) is list) or (type(j_object) is set) or (type(j_object) is tuple):
        new_str = ''
        for item in j_object:
            new_str += '\n' + current_tab + node_to_str(item, current_tab)
        return new_str

    # если текущий объект является словарем
    if type(j_object) is dict:
        new_str = ''
        # для каждой пары ключ-значение
        for key, value in j_object.items():
            # формируем новую строку
            new_str += '\n' + current_tab + \
                       node_to_str(key, current_tab + '\t') + ' - ' + node_to_str(value, current_tab + '\t')
        return new_str
    # если текущий объект не является коллекцией, просто возвращаем его в строковой форме
    return str(j_object)


# функция принимает на вход имя json-файла
def print_json_file(json_file):
    with open(json_file) as f:
        sample = json.load(f)
    print(node_to_str(sample, ''))
    return


print_json_file('example_2.json')
