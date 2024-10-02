from enum import Enum


class Token():
    def __init__(self, token_type: str, value: str, line_num: int):
        self.token_type = token_type
        self.value = value
        self.line = line_num

    def to_string(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '(' + self.token_type + ',"' + self.value + '",' + str(self.line) + ')'
