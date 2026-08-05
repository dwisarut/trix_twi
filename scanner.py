from token_type import TokenType
from trix import error
from token_class import Token

KEYWORDS = {
    # boolean algebra
    "and": TokenType.AND,
    "or": TokenType.OR,
    
    # Control flow
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    
    # bool
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    
    # Loop
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    
    # Declaration, function, and type
    "func": TokenType.FUNC,
    "var": TokenType.VAR,
    "print": TokenType.PRINT,
    "null": TokenType.NULL,
    "return": TokenType.RETURN,
    
    # OOP related
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "class": TokenType.CLASS,
}

class Scanner:
    start = 0
    current = 0
    line = 1
    
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
    
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scan_token(self):
        c = self.advance()
        
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '+': self.add_token(TokenType.PLUS)
            case '-': self.add_token(TokenType.MINUS)
            case ';': self.add_token(TokenType.SEMI_COLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case (' ', '\r', '\t'): pass
            case '\n': self.line += 1
            case '"': self.string_literal()
            
            case _:
                if self.is_digit(c):
                    self.number_literal()
                elif self.is_alphabet(c):
                    self.identifier()
                else:
                    error(self.line, "Unexpected character.")
    
    def string_literal(self):
        while not self.is_at_end():
            if self.peek() == '"':
                break
            if self.peek() == '\n':
                self.line += 1
            
            self.advance()

        if self.is_at_end():
            error(self.line, "Unterminated string.")
            return
            
        self.advance()
        
        val = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, val)
    
    def number_literal(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
    
            while self.is_digit(self.peek()):
                self.advance()
        
        number = float(self.source[self.start: self.current])
        self.add_token(TokenType.NUMBER, number)
    
    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        
        text = self.source[self.start: self.current]
        t_type = KEYWORDS.get(text)
        
        if t_type is None:
            t_type = TokenType.IDENTIFIER
        
        self.add_token(t_type)
    
    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True
    
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def is_digit(self, c: str):
        return '0' <= c <= '9'
    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def is_alphabet(self, c: str):
        return (
            'a' <= c <= "z" or
            'A' <= c <= "Z" or 
            c == '_'
        )
    
    def is_alpha_numeric(self, c: str):
        return self.is_alphabet(c) or self.is_digit(c)
    
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char
    
    def add_token(self, token_type: TokenType, literal=None):
        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
