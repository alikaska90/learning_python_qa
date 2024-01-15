
def filter_by_dict_key_and_value(data: list, key: str, value: str) -> list:
    return [elem for elem in data if elem[key] == value]


def sort_dicts_by_key(data: list, key: str, reverse: bool = False) -> list:
    return sorted(data, key=lambda x: x[key], reverse=reverse)


def sort_dict_by_value(data: dict, reverse: bool = False) -> list:
    return sorted(data.items(), key=lambda item: item[1], reverse=reverse)


def convert_tuple_list_to_dict_list(data: list, keys: tuple) -> list:
    return [dict(zip(keys, elem)) for elem in data]
