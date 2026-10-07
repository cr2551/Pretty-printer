# Scanner -- lexical analysis for the project's Scheme subset.

from Tokens import Token, TokenType, IntToken, StrToken, IdentToken


class Scanner:
    WHITESPACE = " \t\n\r\f"
    INITIAL = "!$%&*/:<=>?^_~"
    SUBSEQUENT = "+-.@"

    def __init__(self, stream):
        self.In = stream
        self.ch_buf = None

    def read(self):
        if self.ch_buf is None:
            return self.In.read(1)
        ch, self.ch_buf = self.ch_buf, None
        return ch

    def peek(self):
        if self.ch_buf is None:
            self.ch_buf = self.In.read(1)
        return self.ch_buf

    @staticmethod
    def isDigit(ch):
        return "0" <= ch <= "9"

    @classmethod
    def is_valid_initial_ident(cls, ch):
        return bool(ch) and ("a" <= ch.lower() <= "z" or ch in cls.INITIAL)

    @classmethod
    def is_valid_subsequent(cls, ch):
        return bool(ch) and (cls.is_valid_initial_ident(ch)
                             or cls.isDigit(ch) or ch in cls.SUBSEQUENT)

    @classmethod
    def delimiter(cls, ch):
        return not ch or ch in cls.WHITESPACE + '();"'

    def getNextToken(self):
        while True:
            ch = self.read()
            if not ch:
                return None
            if ch in self.WHITESPACE:
                continue
            if ch == ";":
                while ch and ch not in "\r\n":
                    ch = self.read()
                continue
            break

        punctuation = {"(": TokenType.LPAREN, ")": TokenType.RPAREN,
                       "'": TokenType.QUOTE}
        if ch in punctuation:
            return Token(punctuation[ch])
        if ch == '"':
            chars = []
            while True:
                ch = self.read()
                if not ch:
                    raise SyntaxError("Unexpected EOF in string")
                if ch == '"':
                    return StrToken("".join(chars))
                if ch == "\\":
                    ch = self.read()
                    if ch not in ('"', "\\"):
                        raise SyntaxError("Expected escaped quote or backslash in string")
                chars.append(ch)

        chars = [ch]
        while not self.delimiter(self.peek()):
            chars.append(self.read())
        word = "".join(chars)
        lower = word.lower()
        if lower in ("#t", "#f"):
            return Token(TokenType.TRUE if lower == "#t" else TokenType.FALSE)
        if word == ".":
            return Token(TokenType.DOT)
        if all(self.isDigit(c) for c in word):
            return IntToken(int(word))
        if (word in ("+", "-", "...") or
                (self.is_valid_initial_ident(word[0]) and
                 all(self.is_valid_subsequent(c) for c in word[1:]))):
            return IdentToken(lower)
        raise SyntaxError("Invalid token: " + repr(word))
