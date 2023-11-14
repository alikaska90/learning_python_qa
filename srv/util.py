from jsonschema import validate, ValidationError


def wrong_elements(collection, substring, lower=False):
    return [elem for elem in collection if not is_substring(elem, substring, lower)]


def is_substring(string, substring, lower):
    if lower:
        string = string.lower()
        substring = substring.lower()
    return substring in string


def default_value_for_less_min_or_more_max(min_value, max_value, curr_value):
    if curr_value < min_value:
        return min_value

    if curr_value > max_value:
        return max_value

    return curr_value


def json_validation(obj, schema):
    try:
        validate(obj, schema)
    except ValidationError as error:
        raise AssertionError from error
    return True
