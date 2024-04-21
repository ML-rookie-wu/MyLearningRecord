import json


def hex_to_int(hex_string):
    try:
        if hex_string.startswith("0x") or hex_string.startswith('-0x'):
            return int(hex_string, 16)
    except ValueError:
        pass
    finally:
        return hex_string

def parse_hex_strings(item):
    if isinstance(item, dict):
        return {key: parse_hex_strings(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [parse_hex_strings(value) for value in item]
    elif isinstance(item, str):
        return hex_to_int(item)
    return item

def json_to_dict(json_string):
    parsed_dict = json.loads(json_string)
    return parse_hex_strings(parsed_dict)

class ParamParser:
    def __init__(self):
        pass

    @staticmethod
    def to_u8(x):
        if x is None:
            return 0xFF
        else:
            return x

    @staticmethod
    def to_list(x):
        if x is None:
            return None
        if isinstance(x, list):
            return x
        elif isinstance(x, str):
            return eval(x)

    @staticmethod
    def to_dict(x):
        if x is None or isinstance(x, dict):
            return x
        elif isinstance(x, str):
            return json_to_dict(x)

    @staticmethod
    def to_int(x):
        if x is None or isinstance(x, int):
            return x
        if isinstance(x, float):
            return int(x)
        elif isinstance(x, str):
            x = x.upper()
            if x[:2] == "0X":
                return int(x, 16)
            elif x[:2] == "0B":
                return int(x, 2)
            elif x.isdigit():
                return int(x)
            else:
                return None