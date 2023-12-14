def create_dict_list_from_string_list(keys: list, data: list) -> list:
    return [dict(zip(keys, line.split())) for line in data]


def cut_string(string: str, num_char: int) -> str:
    if len(string) > num_char:
        return string[:num_char]
    return string


def get_dict_with_max_value(dict_list: list, value: str) -> dict:
    new_dict_list = sorted(dict_list, key=lambda x: x[value])
    return new_dict_list[-1]


def get_value_list_by_dict_key(dict_list: list, key: str, unic: bool = False) -> list:
    result_list = [elem[key] for elem in dict_list]
    if unic:
        result_list = list(dict.fromkeys(result_list))
    return result_list
