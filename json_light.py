from typing import List, Optional, Union


class Data:
    def __init__(self, string):
        self.string = string
        self.idx = 0

    def end(self) -> bool:
        return self.idx >= len(self.string)

    def next(self) -> Optional[str]:
        if not self.end():
            self.idx += 1
            return self.string[self.idx - 1]
        return None

    def current(self) -> Optional[str]:
        return None if self.end() else self.string[self.idx]

    def check(self, char: List[str]) -> bool:
        if not self.end() and self.string[self.idx] in char:
            self.next()
            return True
        return False

    def expect(self, chars: List[str], default=None) -> Optional[str]:
        if not self.end() and self.string[self.idx] in chars:
            self.next()
            return self.string[self.idx - 1]
        return default

    def expect_list(self, chars: List[str]) -> str:
        lst = ""
        while (char := self.expect(chars)) is not None:
            lst += char
        return lst


class JSONLightParsingException(Exception):
    pass


def skip_whitespace(data: Data):
    """
    Skips all whitespace characters (space, tab, new-line, carriage return)
    >>> d = Data(' \\t\\n \\rt'); skip_whitespace(d); d.current()
    't'
    """
    data.expect_list([' ', '\t', '\n', '\r'])


def parse_string(data: Data) -> str:
    """
    >>> parse_string(Data('"\\u041F\\u0430\\u0439\\u0442\\u043E\\u043D1\"'))
    'Пайтон1'
    """
    data.next()
    string = ""
    while (char := data.next()) != '\"':
        if char != '\\':
            string += char
        else:
            control = data.next()
            if control == 'u':
                string += chr(int(''.join([data.next() for _ in range(4)]), 16))
            elif control == 'n':
                string += '\n'
            elif control == 'b':
                string += '\b'
            elif control == 'f':
                string += '\f'
            elif control == 'r':
                string += '\r'
            elif control == 't':
                string += '\t'
            elif control == '\"':
                string += '\"'
            elif control == '/':
                string += '/'
    return string


def parse_number(data: Data) -> Union[float, int]:
    """
    >>> parse_number(Data("-0.121e-2"))
    -0.00121
    >>> parse_number(Data("6526.9"))
    6526.9
    >>> parse_number(Data("-56"))
    -56
    """
    sign = -1 if data.check(['-']) else 1
    digits = list(map(str, range(0, 10)))
    integer = '0' if data.check(['0']) else data.expect_list(digits)
    fraction = float(f'0.{data.expect_list(digits)}') if data.check(['.']) else 0
    exponent = (data.expect(['+', '-'], '') + data.expect_list(digits)) if data.check(['e', 'E']) else '0'

    return sign * (int(integer) + fraction) * (10 ** int(exponent))


def parse_token(data: Data, pattern: str) -> bool:
    """
    >>> parse_token(Data("false, "), "false")
    True
    """
    for ch in pattern:
        if data.next() != ch:
            return False
    return True


def parse_array(data: Data):
    arr = []
    while data.next() in ['[', ',']:
        skip_whitespace(data)
        if data.current() == ']':
            data.next()
            break
        arr.append(parse_value(data))
    return arr


def parse_object(data: Data):
    dct = {}
    while data.next() in ['{', ',']:
        skip_whitespace(data)
        if data.current() == '}':
            data.next()
            break
        key = parse_string(data)
        skip_whitespace(data)
        data.expect([':'])
        dct[key] = parse_value(data)
    return dct


def parse_value(data: Data):
    skip_whitespace(data)
    value = None
    if data.current() == '\"':
        value = parse_string(data)
    elif data.current().isdigit() or data.current() == '-':
        value = parse_number(data)
    elif data.current() == 't':
        value = parse_token(data, 'true')
    elif data.current() == 'f':
        value = parse_token(data, 'false')
    elif data.current() == 'n':
        value = parse_token(data, 'null')
    elif data.current() == '{':
        value = parse_object(data)
    elif data.current() == '[':
        value = parse_array(data)
    skip_whitespace(data)
    return value


def parse(string: str):
    try:
        return parse_value(Data(string))
    except Exception as e:
        raise JSONLightParsingException(e)
