import re


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def variable(self):
        result = ''
        while self.current_char is not None and re.match(r'[a-zA-Z_]', self.current_char):
            result += self.current_char
            self.advance()
        return ('VARIABKE', result)

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', int(result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if re.match(r'[a-zA-Z_]', self.current_char):
                return self.variable()
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            self.error()
        return ('EOF', None)
