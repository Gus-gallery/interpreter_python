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


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def factor(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.current_token = self.lexer.get_next_token()
            return Num(token)
        self.error()

    def term(self):
        node = self.factor()
        while self.current_token[0] == 'PLUS':
            token = self.current_token
            self.current_token = self.lexer.get_next_token()
            node = BinOp(node, token, self.factor())
        return node

    def parse(self):
        return self.term()
