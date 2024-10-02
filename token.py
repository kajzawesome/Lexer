class Token():
    def __init__(self, token_type: str, value: str, line_num: int):
        self.token_type = token_type
        self.value = value
        self.line = line_num

    def to_string(self) -> str:
        output_token: str = "(" + self.token_type + ",\"" + self.value + "\"," + str(self.line) + ")"
        return output_token